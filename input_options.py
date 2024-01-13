import os
import sys
from util import fflogger
from abc import ABC, abstractmethod
from media_stream import VideoStream, AudioStream, SubtitleStream, DataStream, MediaStreamBuilder
from typing import List
logger = fflogger.getLogger(__name__)

class InputOptionsBuilder(ABC):

    @abstractmethod
    def getOptions():
        pass

class BaseInputOptions(InputOptionsBuilder):

    _file_name: str = None
    _default_input_option : list = ['-i']
    _media_stream_builder: MediaStreamBuilder = None

    # TODO: GlobalOptionBuilder instance to be added
    # *Might Autobox for convenience eg Videos composing _videos: List[VideoStream]
    _videos: List[VideoStream] = None
    _audios: List[AudioStream] = None
    _subtitle_streams: List[SubtitleStream] = None
    _data_streams: List[DataStream] = None

    def __init__(self, file_name) -> None:
        super().__init__()
        self._file_name = file_name
        self._media_stream_builder = MediaStreamBuilder(self._file_name)
        self._videos = self._media_stream_builder.videos
        self._audios = self._media_stream_builder.audios
        self._subtitle_streams = self._media_stream_builder.subtitle_streams
        self._data_streams = self._media_stream_builder.data_streams

    def describe(self):
        for video in self._videos:
            print(video)
        for audio in self._audios:
            print(audio)
        for subtitle in self._subtitle_streams:
            print(subtitle)
        for data in self._data_streams:
            print(data)

    def getOptions():
        pass






