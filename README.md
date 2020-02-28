# pyd2v

A Python Parser for DGMPGDec's D2V Project Files

`pip install pyd2v`

<p align="center">
<a href="https://python.org"><img src="https://img.shields.io/badge/python-3.6%2B-informational?style=flat-square" /></a>
<a href="https://github.com/rlaPHOENiX/pyd2v/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/rlaPHOENiX/pyd2v?style=flat-square"></a>
<a href="https://www.codefactor.io/repository/github/rlaphoenix/pyd2v"><img src="https://www.codefactor.io/repository/github/rlaphoenix/pyd2v/badge" alt="CodeFactor" /></a>
<a href="https://www.codacy.com/manual/rlaPHOENiX/pyd2v?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rlaPHOENiX/pyd2v&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/d4f765fcf63249f78c156f2ecc980010"/></a>
<a href="https://github.com/rlaPHOENiX/pyd2v/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/rlaPHOENiX/pyd2v?style=flat-square"></a>
<a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>
</p>

## Documentation

### Quick Example

```
# pip install pyd2v
from pyd2v import D2V

# ...

# Choose Input File
input_file = "/home/user/Desktop/video.d2v"
# Parse Input File
d2v = D2V(filename=input_file)
# Print D2V Version and Settings Options, which will be shown with the accessible variable names.
print(d2v)
# Print Input Video Files
print(d2v.videos)
# Print Frame Rate
print(d2v.settings["Frame_Rate"])
# Print first frame data
print(d2v.data[0])
```

#### Accessible Variables

A successful D2V parse will result in the following options accessible from the D2V object.

- version: D2V version, `16` is currently the latest for the original DGIndex which was last updated in 2010.
- videos: List of the video file paths that were indexed by DGIndex. It will be just a filename if "Use Full Paths" was disabled in DGIndex.
- settings: Will return various user-provided and auto-evaluated settings based on input data. More information on Settings below.
- data: Indexing data of the MPEG video stream, Each entry is of an I frame which will describe the following non-I frames up to the next I frame.
- data_type: What type of video is most previlent, e.g. `88.4% FILM`, `PAL`, `99.9% NTSC`.

#### Settings

| Auto-evaluated Settings | Possible Values                        | Description                                                                        |
| ----------------------- | -------------------------------------- | ---------------------------------------------------------------------------------- |
| Stream_Type             | 0=Elementary Stream                    | Defines the type of MPEG stream.                                                   |
|                         | 1=Program Stream                       |                                                                                    |
|                         | 2=Transport Stream                     |                                                                                    |
|                         | 3=PVA Stream                           |                                                                                    |
| Transport_Packet_Size   | [188, 204]                             | Specifies the size in bytes of the transport packets. Used only for Stream_Type=2. |
| MPEG_Type               | 1=MPEG-1, 2=MPEG-2                     | Defines the type of MPEG stream.                                                   |
| Aspect_Ratio            | MPEG-2: "1:1", "4:3", "16:9", "2.21:1" | Defines the Aspect Ratio of the video specified in the MPEG stream.                |
|                         | MPEG-1: "1:1", 0.6735, ["16:9", 625],  |                                                                                    |
|                         | 0.7615, 0.8055, ["16:9", 525], 0.8935, |                                                                                    |
|                         | ["4:3", 625], 0.9815, 1.0255, 1.0695,  |                                                                                    |
|                         | ["4:3", 525], 1.575, 1.2015            |                                                                                    |
| Picture_Size            | [width, height]                        | Defines the size of the video _after_ clipping has been applied.                   |
| Frame_Rate              | rate [num, den]                        | 'rate' defines output framerate \* 1000.                                           |

| User-specified Settings | Possible Values                           | Description                                                              |
| ----------------------- | ----------------------------------------- | ------------------------------------------------------------------------ |
| MPEG2_Transport_PID     | {Video, Audio, RCR}                       | Selects the video/audio PIDs to be decoded. Used only for Stream_Type=2. |
| iDCT_Algorithm          | 1=32-bit MMX                              | Defines the iDCT DGDecode will use to decode this video                  |
|                         | 2=32-bit SSEMMX                           |                                                                          |
|                         | 3=32-bit SSE2MMX                          |                                                                          |
|                         | 4=64-bit Floating Point                   |                                                                          |
|                         | 5=64-bit IEEE-1180 Reference              |                                                                          |
|                         | 6=32-bit SSEMMX (Skal)                    |                                                                          |
|                         | 7=32-bit Simple MMX (XviD)                |                                                                          |
| YUVRGB_Scale            | 0=TV Scale                                | Defines the range DGDecode will use if RGB conversion is requested.      |
|                         | 1=PC Scale                                |                                                                          |
| Luminance_Filter        | {Gamma, Offset} (range of +/- 256)        | Defines values for DGIndex's Luminance_Filter.                           |
| Clipping                | [ClipLeft,ClipRight,ClipTop,ClipBottom]   | Defines values for Cropping lines of video.                              |
| Field_Operation         | 0=Honor Pulldown Flags                    | Defines values for Field Operation.                                      |
|                         | 1=Force Film                              |                                                                          |
|                         | 2=Ignore Pulldown Flags                   |                                                                          |
| Location                | {StartFile,StartOffset,EndFile,EndOffset} | Defines start and end points for the video selection range.              |
