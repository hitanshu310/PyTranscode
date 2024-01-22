import os
import sys
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from stream_info import StreamInfo
from util import fflogger
logger = fflogger.getLogger(__name__)


class StreamSpeciferInterface(ABC):

    @abstractmethod
    def streamSpecifier(self):
        pass

class MediaStream(StreamSpeciferInterface):

    _stream_specifier: str = None
    _stream_relative_index = None
    _index: int = None
    _codec_type: str = None
    _codec_tag_string: str = None
    _codec_tag : str = None
    _stream_specifier_code = None
    _init_dictionary: dict = None
    _input_id : int = 0

    # *Initializes varaibles from dicationary if available
    def __init__(self, init_dictionary: dict, stream_relative_index: int, input_id: int  = 0):
        self._stream_relative_index = stream_relative_index
        self._index = init_dictionary['index']
        self._codec_type = init_dictionary['codec_type']
        self._codec_tag_string = init_dictionary['codec_tag_string']
        self._codec_tag = init_dictionary['codec_tag']
        self._input_id = input_id

    def __repr__(self):
        repr_dict = {}
        repr_dict['stream_relative_index'] = self._stream_relative_index
        repr_dict['index'] = self._index
        repr_dict['codec_type'] = self._codec_type
        repr_dict['codec_tag_string'] = self._codec_tag_string
        repr_dict['codec_tag'] = self._codec_tag
        return str(repr_dict)

    @abstractmethod
    def streamSpecifier(self):
        pass

class VideoStream(MediaStream):

    def __init__(self, init_dictionary: dict, relative_index):
        super().__init__(init_dictionary, relative_index)
        self._init_dictionary = init_dictionary
        self._codec_name = init_dictionary['codec_name']
        self._codec_long_name = init_dictionary['codec_long_name']
        self._stream_specifier_code = "v"
        
    def streamSpecifier(self):
        return [":v"] + [str(self._index)]

class AudioStream(MediaStream):

    def __init__(self, init_dictionary: dict, relative_index):
        super().__init__(init_dictionary, relative_index)
        self._init_dictionary = init_dictionary
        self._codec_name = init_dictionary['codec_name']
        self._codec_long_name = init_dictionary['codec_long_name']
        self._stream_specifier_code = "a"

    def streamSpecifier(self):
        pass

class SubtitleStream(MediaStream):

    def __init__(self, init_dictionary: dict, relative_index):
        super().__init__(init_dictionary, relative_index)
        self._init_dictionary = init_dictionary
        self._codec_name = init_dictionary['codec_name']
        self._codec_long_name = init_dictionary['codec_long_name']
        self._stream_specifier_code = "s"

    def streamSpecifier(self):
        pass


class DataStream(MediaStream):

    def __init__(self, init_dictionary: dict, relative_index):
        super().__init__(init_dictionary, relative_index)
        self._init_dictionary
        self._stream_specifier_code = "d"

    def streamSpecifier(self):
        pass
"""
class Videos(StreamSpeciferInterface):

    _count = None
    _videos: List[VideoStream] = None

    def __init__(self) -> None:
        super().__init__()
        self._count = -1
        self._videos = list()

    def addVideoStream(self, stream_data: dict):
        self._count = self._count + 1
        self._videos.append(VideoStream(stream_data, self._count))

    def __iter__(self):
        return self._videos.__iter__()

    def getVideoStream(self, index: int):
        return self._videos[index]

    def streamSpecifier(self):
        return [":v"]
"""    
T = TypeVar("T", bound=MediaStream)

class MediaStreamCollection(StreamSpeciferInterface, Generic[T]):

    _count: int = None
    _streams: List[T] = list()

    def __init__(self) -> None:
        super().__init__()
        self._count = -1
        self._streams = list()

    @abstractmethod
    def addStream(self, stream_data: dict):
        self._count = self._count + 1

    def __iter__(self):
        return self._streams.__iter__()
    
    def getStream(self, index: int):
        return self._streams[index]

    @abstractmethod
    def streamSpecifier(self):
        pass

class Videos(MediaStreamCollection):

    _streamSpecifierString = None

    def __init__(self) -> None:
        super().__init__()
        self._streamSpecifierString = "v"

    def addStream(self, stream_data: dict):
        super().addStream(stream_data)
        self._streams.append(VideoStream(stream_data, self._count))

    def streamSpecifier(self):
        return ":"+self._streamSpecifierString
    
class Audios(MediaStreamCollection):

    _streamSpecifierString = None

    def __init__(self) -> None:
        super().__init__()
        self._streamSpecifierString = "a"

    def addStream(self, stream_data: dict):
        super().addStream(stream_data)
        self._streams.append(AudioStream(stream_data, self._count))

    def streamSpecifier(self):
        return ":"+self._streamSpecifierString
    
class SubtitleStreams(MediaStreamCollection):

    _streamSpecifierString = None

    def __init__(self) -> None:
        super().__init__()
        self._streamSpecifierString = "s"

    def addStream(self, stream_data: dict):
        super().addStream(stream_data)
        self._streams.append(SubtitleStream(stream_data, self._count))

    def streamSpecifier(self):
        return ":"+self._streamSpecifierString

class DataStreams(MediaStreamCollection):

    _streamSpecifierString = None

    def __init__(self) -> None:
        super().__init__()
        self._streamSpecifierString = "d"

    def addStream(self, stream_data: dict):
        super().addStream(stream_data)
        self._streams.append(DataStream(stream_data, self._count))

    def streamSpecifier(self):
        return ":"+self._streamSpecifierString

# *Generates media streams from input file
class MediaStreamBuilder():

    _file_name: str = None
    _streams: StreamInfo = None
    _videos: Videos = None
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
        self._videos = Videos()
        self._audios = Audios()
        self._subtitle_streams = SubtitleStreams()
        self._data_streams = DataStreams()
        self._file_name = file_name
        self.streams = StreamInfo(self._file_name)
        self.parseStreamInfo(self.streams._stream_info)

    def parseStreamInfo(self, stream_info_dictionary):
        for stream in stream_info_dictionary['streams']:
            if stream['codec_type'] == 'video':
                self._videos.addStream(stream)
            elif stream['codec_type'] == 'audio':
                self._audios.addStream(stream)
            elif stream['codec_type'] == 'subtitle':
                self._subtitle_streams.addStream(stream)
            else:
                data_stream = DataStream(stream, 1)
                self._data_streams.addStream(stream)






