from typing import Any
from collections.abc import Callable
import math
from pathlib import PurePath
from langchain.docstore.document import Document
from .basevideo import BaseVideoLoader


def split_text(text, max_length):
    """Split text into chunks of a maximum length, ensuring not to break words."""
    chunks = []
    while len(text) > max_length:
        # Find the last space before the max_length
        split_point = text.rfind(' ', 0, max_length)
        # If no space found, split at max_length
        if split_point == -1:
            split_point = max_length
        chunks.append(text[:split_point])
        text = text[split_point:].strip()
    chunks.append(text)
    return chunks


class VideoLocalLoader(BaseVideoLoader):
    """
    Generating Video transcripts from local Videos.
    """
    _extension = ['.mp4', '.webm']

    def __init__(
        self,
        path: PurePath,
        tokenizer: Callable[..., Any] = None,
        text_splitter: Callable[..., Any] = None,
        source_type: str = 'documentation',
        encoding: str = 'utf-8',
        origin: str = '',
        **kwargs
    ):
        super().__init__(tokenizer, text_splitter, source_type=source_type, **kwargs)
        self.path = path

    def load_video(self, path: PurePath) -> list:
        metadata = {
            "url": f"{path.name}",
            "source": f"{path}",
            "filename": f"{path}",
            "index": path.stem,
            "question": '',
            "answer": '',
            'type': 'video_transcript',
            "source_type": self._source_type,
            "data": {},
            "summary": '',
            "document_meta": {
                "language": self._language,
                "topic_tags": ""
            }
        }
        documents = []
        transcript_path = path.with_suffix('.vtt')
        audio_path = path.with_suffix('.mp3')
        # second: extract audio from File
        self.extract_audio(path, audio_path)
        # get the Whisper parser
        transcript_whisper = self.get_whisper_transcript(audio_path)
        if transcript_whisper:
            transcript = transcript_whisper['text']
        else:
            transcript = ''
        # Summarize the transcript
        if transcript:
            # Split transcript into chunks
            transcript_chunks = split_text(transcript, 32767)
            summary = self.get_summary_from_text(transcript)
            # Create Two Documents, one is for transcript, second is VTT:
            metadata['summary'] = summary
            for chunk in transcript_chunks:
                doc = Document(
                    page_content=chunk,
                    metadata=metadata
                )
                documents.append(doc)
        if transcript_whisper:
            # VTT version:
            transcript = self.transcript_to_vtt(transcript_whisper, transcript_path)
            transcript_chunks = split_text(transcript, 65535)
            for chunk in transcript_chunks:
                doc = Document(
                    page_content=chunk,
                    metadata=metadata
                )
                documents.append(doc)
            # Saving every dialog chunk as a separate document
            dialogs = self.transcript_to_blocks(transcript_whisper)
            docs = []
            for chunk in dialogs:
                _meta = {
                    "index": f"{path.stem}:{chunk['id']}",
                    "document_meta": {
                        "start": f"{chunk['start_time']}",
                        "end": f"{chunk['end_time']}",
                        "id": f"{chunk['id']}",
                        "language": self._language,
                        "title": f"{path.stem}",
                        "topic_tags": ""
                    }
                }
                _info = {**metadata, **_meta}
                doc = Document(
                    page_content=chunk['text'],
                    metadata=_info
                )
                docs.append(doc)
            documents.extend(docs)
        return documents

    def load(self) -> list:
        documents = []
        if self.path.is_file():
            docs = self.load_video(self.path)
            documents.extend(docs)
        if self.path.is_dir():
            # iterate over the files in the directory
            for ext in self._extension:
                for item in self.path.glob(f'*{ext}'):
                    if set(item.parts).isdisjoint(self.skip_directories):
                        documents.extend(self.load_video(item))
        return self.split_documents(documents)

    def extract(self) -> list:
        documents = []
        if self.path.is_file():
            docs = self.load_video(self.path)
            documents.extend(docs)
        if self.path.is_dir():
            # iterate over the files in the directory
            for ext in self._extension:
                for item in self.path.glob(f'*{ext}'):
                    if set(item.parts).isdisjoint(self.skip_directories):
                        documents.extend(self.load_video(item))
        return documents
