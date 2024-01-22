# PyTranscode
## Python bindings for ffmpeg
A pythonic way to build ffmpeg command line arguments for video transcoding. Provides an intuitive mapping and stream selection interface. Easily extendable and easy to use. Uses ffmpeg packages for linux.
## [Install ffmpeg for linux](https://ffmpeg.org/download.html#build-linux)
PyTranscode requires ffmpeg binaries to be installed on the linux to be used.
## ffmpeg command structure
```
ffmpeg [global_options] {[input_file_options] -i input_url} ..{[output_file_options] output_url} ...
```
## How ffmpeg works
The transcoding process in **`ffmpeg`** for each output can be described by the following diagram:
<img src="ffmpeg_stream_diagram.drawio.png" width="100%"/>
Ffmpeg working as described by `man ffmpeg`
> Ffmpeg calls the libavformat library to read input files and get packets containing encoded data from them. When there are multiple input files, ffmpeg tries to keep them synchronized by tracking lowest timestamp on any active input stream. 
<br><br>
Encoded packets are then passed to the decoder. The decoder produces uncompressed frames (raw video/PCM audio/...) which can be processed further by filtering. After filtering, the frames are passed to the encoder, which encodes them and outputs encoded packets. Finally those are passed to the muxer, which writes the encoded packets to the output file.