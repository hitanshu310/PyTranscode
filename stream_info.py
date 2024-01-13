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

    # *Important: Temporary initialization
    # TODO: Initialize with global options option
    _global_options: list = ['-hide_banner', '-print_format', 'json']
    
    def commandBuilder(self):
        logger.info(self._binary + self._global_options + self._metadata_option)
        self._command = self._binary + self._global_options + self._metadata_option + [self._filename]
        command = Command(self._command)
        command.execute()

        if command.returncode == 0:
            logger.info(json.loads(command.stdout))
        else:
            logger.error(command.stderr.decode())

if __name__ == "__main__":
    info  = StreamInfo('GX010626.MP4')
    info.commandBuilder()


