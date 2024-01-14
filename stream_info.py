import json
from util import Command
from util import fflogger
logger = fflogger.getLogger(__name__)

class StreamInfo():

    _stream_info: dict = None
    _binary: str = ['ffprobe']
    _metadata_option = ['-show_streams']
    _command: list = []
    
    def __init__(self, fileName: str):
        self._filename = fileName
        self.commandBuilder()

    # *Important: Temporary initialization
    # TODO: Initialize with global options option
    _global_options: list = ['-hide_banner', '-v', 'quiet', '-print_format', 'json']
    
    def commandBuilder(self):
        logger.info(self._binary + self._global_options + self._metadata_option)
        self._command = self._binary + self._global_options + self._metadata_option + [self._filename]
        command = Command(self._command)
        command.execute()

        if command.returncode == 0:
            self._stream_info = json.loads(command.stdout)
            logger.info(self._stream_info)
        else:
            logger.error(command.stderr.decode())



