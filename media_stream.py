import os
import sys
from abc import ABC, abstractmethod
from typing import List
from stream_info import StreamInfo
from util import fflogger
logger = fflogger.getLogger(__name__)

class MediaStream(ABC):

    _stream_specifier: str = None
    _index: int = None
    _codec_type: str = None
    _codec_tag_string: str = None
    _codec_tag : str = None
    _stream_specifier_code = None
    _init_dictionary: dict = None
    _input_id : int = 0

    # *Initializes varaibles from dicationary if available
    def __init__(self, init_dictionary: dict, input_id: int  = 0):
        self._index = init_dictionary['index']
        self._codec_type = init_dictionary['codec_type']
        self._codec_tag_string = init_dictionary['codec_tag_string']
        self._codec_tag = init_dictionary['codec_tag']
        self._input_id = input_id

    def __repr__(self):
        repr_dict = {}
        repr_dict['index'] = self._index
        repr_dict['codec_type'] = self._codec_type
        repr_dict['codec_tag_string'] = self._codec_tag_string
        repr_dict['codec_tag'] = self._codec_tag
        return str(repr_dict)

    @abstractmethod
    def streamSpecifier():
        pass

class VideoStream(MediaStream):

    def __init__(self, init_dictionary: dict):
        super().__init__(init_dictionary)
        self._init_dictionary = init_dictionary
        self._codec_name = init_dictionary['codec_name']
        self._codec_long_name = init_dictionary['codec_long_name']
        self._stream_specifier_code = "v"
        
    def streamSpecifier():
        pass

class AudioStream(MediaStream):

    def __init__(self, init_dictionary: dict):
        super().__init__(init_dictionary)
        self._init_dictionary = init_dictionary
        self._codec_name = init_dictionary['codec_name']
        self._codec_long_name = init_dictionary['codec_long_name']
        self._stream_specifier_code = "a"

    def streamSpecifier():
        pass

class SubtitleStream(MediaStream):

    def __init__(self, init_dictionary: dict):
        super().__init__(init_dictionary)
        self._init_dictionary = init_dictionary
        self._codec_name = init_dictionary['codec_name']
        self._codec_long_name = init_dictionary['codec_long_name']
        self._stream_specifier_code = "s"

    def streamSpecifier():
        pass


class DataStream(MediaStream):

    def __init__(self, init_dictionary: dict):
        super().__init__(init_dictionary)
        self._init_dictionary
        self._stream_specifier_code = "d"

    def streamSpecifier():
        pass

# *Generates media streams from input file
class MediaStreamBuilder():

    _file_name: str = None
    _streams: StreamInfo = None
    _videos: List[VideoStream] = []
    _audios: List[AudioStream] = []
    _subtitle_streams: List[SubtitleStream] = []
    _data_streams: List[DataStream] = []

    @property
    def videos(self):
        return self._videos
    
    @property
    def audios(self):
        return self._audios
    
    @property
    def subtitle_streams(self):
        return self._subtitle_streams
    
    @property
    def data_streams(self):
        return self._data_streams

    def __init__(self, file_name) -> None:
        self._file_name = file_name
        self.streams = StreamInfo(self._file_name)
        self.parseStreamInfo(self.streams._stream_info)

    def parseStreamInfo(self, stream_info_dictionary):
        for stream in stream_info_dictionary['streams']:
            if stream['codec_type'] == 'video':
                video_stream = VideoStream(stream)
                self._videos.append(video_stream)
            elif stream['codec_type'] == 'audio':
                audio_stream = AudioStream(stream)
                self._audios.append(audio_stream)
            elif stream['codec_type'] == 'subtitle':
                subtitle_stream = SubtitleStream(stream)
                self._subtitle_streams.append(subtitle_stream)
            else:
                data_stream = DataStream(stream)
                self._data_streams.append(data_stream)
        




