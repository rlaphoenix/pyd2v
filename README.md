# pyd2v

[![License](https://img.shields.io/github/license/rlaphoenix/pyd2v)](https://github.com/rlaphoenix/pyd2v/blob/master/LICENSE)
[![Build status](https://github.com/rlaphoenix/pyd2v/actions/workflows/ci.yml/badge.svg)](https://github.com/rlaphoenix/pyd2v/actions/workflows/ci.yml)
[![Python version](https://img.shields.io/pypi/pyversions/pyd2v)](https://pypi.python.org/pypi/pyd2v)
[![PyPI version](https://img.shields.io/pypi/v/pyd2v)](https://pypi.python.org/pypi/pyd2v)
[![Contributors](https://img.shields.io/github/contributors/rlaphoenix/pyd2v)](https://github.com/rlaphoenix/pyd2v/graphs/contributors)
[![DeepSource issues](https://deepsource.io/gh/rlaphoenix/pyd2v.svg/?label=active+issues)](https://deepsource.io/gh/rlaphoenix/pyd2v)

A Python Parser for DGMPGDec's D2V Project Files.

## Installation

    pip install --user pyd2v

## Building

### Dependencies

- [Python](https://python.org/downloads) (v3.7 or newer)
- [Poetry](https://python-poetry.org/docs) (latest recommended)

### Steps

1. `git clone https://github.com/rlaphoenix/pyd2v`
2. `cd pyd2v`
3. `poetry config virtualenvs.in-project true` (optional, but recommended)
4. `poetry install`
5. `d2v --help`

For further information on using the Poetry virtual environment, see
[Using your virtual environment](https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment).

## Usage

This project can be used in Python Scripts by importing `pyd2v`, or in your terminal by calling `d2v`.

### Scripting

```py
from pyd2v import D2V

# ...

d2v = D2V(filename="C:/Users/phoenix/Videos/1998_home_video.d2v")
print(d2v)  # d2v object basic information, e.g. version and settings
print(d2v.videos)  # input video files
print(d2v.settings["Frame_Rate"])  # frame rate
print(d2v.data[0])  # print first frame data
```

### Executable

For help information run `d2v --help`. Here's some examples of using the d2v executable:

#### Getting a Setting like the Video Resolution:

```shell
$ d2v "D:\...\The.IT.Crowd.S01E01.Yesterdays.Jam.PAL.DVD.DD.2.0.MPEG-2.REMUX.d2v" settings.Picture_Size
[720, 576]
```

#### Parse the entire D2V to a JSON Pickle:

```shell
$ d2v "D:\...\The.IT.Crowd.S01E01.Yesterdays.Jam.PAL.DVD.DD.2.0.MPEG-2.REMUX.d2v" --json
{"py/object": "pyd2v.d2v.D2V", "path": {"py/reduce": [{"py/type": "pathlib.WindowsPath"}, {"py/tuple": ["D:\\", "...",
"The.IT.Crowd.S01E01.Yesterdays.Jam.PAL.DVD.DD.2.0.MPEG-2.REMUX.d2v"]}]}, "version": 16, "videos": [
"D:\\...\\The.IT.Crowd.S01E01.Yesterdays.Jam.PAL.DVD.DD.2.0.MPEG-2.REMUX.mpeg"], "settings": {"Stream_Type": 0,
"MPEG_Type": 2, "iDCT_Algorithm": 5, "YUVRGB_Scale": 1, "Luminance_Filter": {"Gamma": 0, "Offset": 0}, "Clipping":
[0, 0, 0, 0], "Aspect_Ratio": "16:9", "Picture_Size": [720, 576], "Field_Operation": 2, ... ...
```

#### Parse only the D2V Headers:

```shell
$ d2v "D:\...\The.IT.Crowd.S01E01.Yesterdays.Jam.PAL.DVD.DD.2.0.MPEG-2.REMUX.d2v" --pretty
<D2V path=WindowsPath('D:/.../The.IT.Crowd.S01E01.Yesterdays.Jam.PAL.DVD.DD.2.0.MPEG-2.REMUX.d2v') version=16,
data_type='100.00% VIDEO\n', settings={'Stream_Type': 0, 'MPEG_Type': 2, 'iDCT_Algorithm': 5, 'YUVRGB_Scale': 1,
'Luminance_Filter': {'Gamma': 0, 'Offset': 0}, 'Clipping': [0, 0, 0, 0], 'Aspect_Ratio': '16:9', 'Picture_Size':
[720, 576], 'Field_Operation': 2, 'Frame_Rate': ['25000', [25, 1]], 'Location': {'StartFile': '0', 'StartOffset': '0',
'EndFile': '0', 'EndOffset': '67d1f'}}>
```

### D2V Properties

D2V objects contain the following properties:

- version: D2V version, `16` is currently the latest for the original DGIndex which was last updated in 2010.
- videos: List of the video file paths that were indexed by DGIndex. It will be just a filename if "Use Full Paths" was
  disabled in DGIndex.
- settings: Will return various user-provided and auto-evaluated settings based on input data. More information on
  Settings below.
- data: Indexing data of the MPEG video stream, Each entry is of an I frame which will describe the following non-I
  frames up to the next I frame.
- data_type: What type of video is most previlent, e.g. `88.4% FILM`, `PAL`, `99.9% NTSC`.

### Settings

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

## License

[MIT License](LICENSE)
