# pyd2v

[![Pull requests welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](http://makeapullrequest.com)
[![MIT license](https://img.shields.io/github/license/rlaPHOENiX/pyd2v?style=flat)](https://github.com/rlaphoenix/pyd2v/blob/master/LICENSE)
[![Python versions](https://img.shields.io/badge/python-3.6%2B-informational)](https://python.org)
[![Codacy rating](https://www.codefactor.io/repository/github/rlaphoenix/pyd2v/badge)](https://www.codefactor.io/repository/github/rlaphoenix/pyd2v)
[![Contributors](https://img.shields.io/github/contributors/rlaphoenix/pyd2v)](https://github.com/rlaphoenix/pyd2v/graphs/contributors)
[![GitHub issues](https://img.shields.io/github/issues/rlaphoenix/pyd2v)](https://github.com/rlaphoenix/pyd2v/issues)

A Python Parser for DGMPGDec's D2V Project Files.

## Installation

    pip install --user pyd2v

### Or, Install from Source

#### Requirements

1. [pip], v19.0 or newer
2. [poetry], latest recommended

#### Steps

1. `poetry config virtualenvs.in-project true` (optional, but recommended)
2. `poetry install`
3. You now have a `.venv` folder in your project root directory. Python and dependencies are installed here.
4. To use the venv, follow [Poetry Docs: Using your virtual environment]

Note: Step 1 is recommended as it creates the virtual environment in one unified location per-project instead of
hidden away somewhere in Poetry's Cache directory.

  [pip]: <https://pip.pypa.io/en/stable/installing>
  [poetry]: <https://python-poetry.org/docs>
  [Poetry Docs: Using your virtual environment]: <https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment>

## Usage

This project can be used programmatically by importing `pyd2v`, and as of version 1.1.0 with a `d2v` call in your terminal.

## Documentation

### Quick Example

```py
from pyd2v import D2V

# ...

d2v = D2V(filename="C:/Users/phoenix/Videos/1998_home_video.d2v")
print(d2v)  # d2v object basic information, e.g. version and settings
print(d2v.videos)  # input video files
print(d2v.settings["Frame_Rate"])  # frame rate
print(d2v.data[0])  # print first frame data
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
