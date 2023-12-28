#!/usr/bin/python3

import os
import sys
import logging
import subprocess
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
encoding_threshold = 3000
constant_rate_factor = 28

def get_encoding_details(fileName):
    if fileName not in os.listdir():
        logger.error(fileName + " not found")
        sys.exit(1)
    else:
        command = "ffprobe -v quiet -print_format json -show_format -show_streams -i"
        args = command.split(' ')
        args.append(fileName)
        logger.info("Args "+' '.join(args))
        p = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0:
            return json.loads(out)
        else:
            logger.error("Command failed")
            sys.exit(1)

def getBitRate(json_metadata):
    return int(json_metadata['format']['bit_rate'])/1024

def getFiles():
    file_list = [file for file in os.listdir() if not (file.endswith('.sh') or file.endswith('.srt'))]
    for file in file_list:
        logger.debug('File name :' + file)
        bit_rate = getBitRate(get_encoding_details(file))
        if bit_rate > encoding_threshold:
            logger.info("Encoding file :" + file + " with bit_rate "  + str(bit_rate))
            encodeFile(file)
        else:
            logger.info("No need to encode")

def encodeFile(fileName):
    file_base_name = ''.join(fileName.split('.')[:-1])
    file_extention = fileName.split('.')[-1]
    temp_file_name = file_base_name + "_h265." + file_extention

    command = "ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i $input_file -c:v hevc_nvenc -crf $crf -c:a copy -c:s copy -map 0 $output_file"
    args = command.split(' ')

    args = map(lambda x: x if x != "$input_file" else fileName, args)
    args = map(lambda x: x if x != "$output_file" else temp_file_name, args)
    args = map(lambda x: x if x != "$crf" else str(constant_rate_factor), args)

    q = subprocess.Popen(args, stdout = subprocess.PIPE)
    out, err = q.communicate()
    logger.debug(out)
    logger.debug("Return Code:" + str(q.returncode))
    if q.returncode == 0:
        logger.debug(out)
        subprocess.run(['rm', fileName])
        subprocess.run(['mv', temp_file_name, fileName])
    else:
        logger.debug(err)

if __name__=="__main__":
    getFiles()