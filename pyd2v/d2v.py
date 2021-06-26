import shutil
import subprocess
from io import StringIO
from pathlib import Path
from typing import TextIO


class D2V:
    """DGIndex D2V project file."""

    def __init__(self, f: TextIO, path: Path = None):
        """
        Parse a d2v.
        :param f: Text IO object of a d2v to be parsed.
        :param path: Path object of the D2V file being parsed.
        :raises ValueError: if parsing fails
        """
        if not isinstance(path, Path) and path is not None:
            raise TypeError(f"D2V path must be a Path object (or None), not {type(path)}")
        if path is not None:
            if not path.exists():
                raise ValueError("D2V path does not exist")
            if not path.is_file():
                raise ValueError("D2V path is to a directory, not a file")
        self.path = path
        self.version = None
        self.videos = None
        self.settings = None
        self.data = None
        self.data_type = None

        """ Header Data """

        self.version = f.readline().strip()
        if not self.version.startswith("DGIndexProjectFile"):
            raise ValueError(f"Expected Version Header, received '{self.version}'")
        self.version = int(self.version[18:])  # strip "DGIndexProjectFile"
        self.videos = [f.readline().strip() for _ in range(int(f.readline().strip()))]

        if len(f.readline().strip()) > 0:
            raise ValueError("Unexpected data after reading Header's Video List.")

        """ Settings Data """

        self.settings = {}
        while True:
            line = f.readline().strip()
            if len(line) == 0:
                break
            key, value = line.split("=", maxsplit=2)
            if key in ["Stream_Type", "MPEG_Type", "iDCT_Algorithm", "YUVRGB_Scale", "Field_Operation"]:
                value = int(value)
            if key in ["MPEG2_Transport_PID", "Transport_Packet_Size", "Luminance_Filter", "Clipping"]:
                value = list(map(int, value.split(",")))
            if key == "MPEG2_Transport_PID":
                value = {"Video": value[0], "Audio": value[1], "PCR": value[2]}
            elif key == "Luminance_Filter":
                value = {"Gamma": value[0], "Offset": value[1]}
            elif key == "Clipping":
                value = list(map(int, value))
            elif key == "Aspect_Ratio":
                if "," in value:
                    value = [(x if ":" in x else float(x)) for x in value.split(",")]
                elif ":" not in value:
                    value = float(value)
            elif key == "Picture_Size":
                value = list(map(int, value.lower().split("x")))
            elif key == "Frame_Rate":
                rate, num_den = value.split(" ")
                num_den = list(map(int, num_den.strip("()").split("/")))
                value = [rate, num_den]
            elif key == "Location":
                start_file, start_offset, end_file, end_offset = value.split(",")
                value = {
                    "StartFile": start_file,
                    "StartOffset": start_offset,
                    "EndFile": end_file,
                    "EndOffset": end_offset
                }
            self.settings[key] = value

        """ Flag Data """

        self.data = []
        while True:
            line = f.readline().strip()
            if len(line) == 0:
                break
            line = line.split(" ", maxsplit=7)
            data = {
                "info": bin(int(line[0], 16))[2:].zfill(8),
                "matrix": line[1],
                "file": int(line[2]),
                "position": int(line[3]),
                "skip": int(line[4]),
                "vob": int(line[5]),
                "cell": int(line[6]),
                "flags": line[7].split(" ")
            }
            data["info"] = {
                "data_line_signal": data["info"][0],
                "part_of_closed_gop": data["info"][1] == "1",
                "part_of_progressive_sequence": data["info"][2] == "1",
                "first_picture_of_new_gop": data["info"][3] == "1",
                "reserved": data["info"][4:]
            }
            if data["flags"][-1].lower() == "ff":
                # ff == end of stream indicator, not an actual frame data byte
                data["flags"] = data["flags"][0:-1]
            data["flags"] = [{
                "require_previous_gop": bit[0] == "0",
                "progressive_frame": bit[1] == "1",
                "picture_coding_type": {
                    "00": "reserved",
                    "01": "I",
                    "10": "P",
                    "11": "B"
                }[bit[2] + bit[3]],
                "reserved_bits": bit[4] + bit[5],
                "tff": bit[6] == "1",
                "rff": bit[7] == "1"
            } for bit in [bin(int(flag, 16))[2:].zfill(8) for flag in data["flags"]]]
            self.data.append(data)
        self.data_type = f.readline()[10:]

    def __repr__(self):
        return f"<D2V version={self.version}, data_type={self.data_type}, settings={self.settings}>"

    @classmethod
    def loads(cls, data: str, path: Path = None):
        """
        Parse a D2V from a blob of string data.

        The optional path argument is available to store the file location of
        the D2V data inside the new D2V object under `D2V.path` class variable.
        It must be a Path object, or otherwise None.
        """
        if not isinstance(path, Path) and path is not None:
            raise TypeError(f"path must be a Path object (or None), not {type(path)}")
        return cls(StringIO(data), path)

    @classmethod
    def load(cls, file: Path):
        """
        Parse a D2V from a file.

        If file is not a D2V path, it will assume it's a path to a video file and
        will generate an optimal D2V from the video file. It will also demux said
        file for D2V generation if it's in a container (e.g., mp4, mkv).

        The generated D2V will be next to the input file, and the direct path will
        be stored within the new D2V object in the `D2V.path` class variable.
        """
        if not isinstance(file, Path):
            raise TypeError(f"file must be a Path object, not {type(file)}")
        if not file.exists():
            raise ValueError("file path does not exist")
        if not file.is_file():
            raise ValueError("file path is to a directory, not a file")
        file = cls._get_d2v(file)
        return cls(file.open(mode="r", encoding="utf8"), file)

    @staticmethod
    def _get_d2v(file_path: Path, idct_algo=5, field_op=2, yuv_to_rgb=1) -> Path:
        """
        Index an optimal D2V file using DGIndex.
        Unix systems are supported as long as Wine is installed.

        Note, It will demux the video track from any containers as DGIndex does
        not support most container formats, and it's generally advised to do so
        even if it does support a specific container.

        The default extra arguments that gets passed to DGIndex is generally
        recommended to be untouched. Especially field_op! Please do not change
        these unless you know what they do. However, you may need to change
        yuv_to_rgb depending on you're source, but most MPEGs should be fine
        set to 1 (PC Scale).
        """
        is_vob = file_path.suffix.lower() == ".vob"
        d2v_path = file_path.with_suffix(".d2v")
        if d2v_path.is_file():
            return d2v_path

        # demux the mpeg stream if not a .VOB or .MPEG file
        demuxed_ext = [".mpeg", ".mpg", ".m2v", ".vob"]
        vid_path = next((x for x in map(file_path.with_suffix, demuxed_ext) if x.exists()), None)
        if not vid_path:
            vid_path = file_path.with_suffix(demuxed_ext[0])
            mkvextract = shutil.which("mkvextract")
            if not mkvextract:
                raise RuntimeError(
                    "Executable 'mkvextract' not found, but is needed for the provided file.\n"
                    "Install MKVToolNix and make sure it's binaries are in the environment path."
                )
            subprocess.run([
                mkvextract,
                file_path.name,
                # TODO: This assumes the track with track-id of 0 is the video. Use pymediainfo to get
                #       first video track's Track ID. For now assuming 0 will have to do.
                "tracks", f"0:{vid_path.name}"
            ], cwd=file_path.parent, check=True)

        # use dgindex to generate a d2v file for the demuxed track
        dgindex = shutil.which("dgindex")
        if not dgindex:
            raise RuntimeError(
                "Executable 'dgindex' not found, but is needed for the provided file.\n"
                "Add dgindex.exe to your environment path. Ensure the executable is named `dgindex.exe`."
            )
        is_unix = dgindex.startswith("/")
        if is_unix:
            # required to do it this way for whatever reason. Directly calling it sometimes fails.
            dgindex = ["wine", "start", "/wait", "Z:" + dgindex]
        else:
            dgindex = [dgindex]
        subprocess.run(
            dgindex + [
                "-ai" if is_vob else "-i", vid_path.name,
                "-ia", idct_algo,  # iDCT Algorithm, 5=IEEE-1180 Reference
                "-fo", field_op,  # Field Operation, 2=Ignore Pulldown Flags
                "-yr", yuv_to_rgb,  # YUV->RGB, 1=PC Scale
                "-om", "0",  # Output Method, 0=None (just d2v)
                "-hide", "-exit",  # start hidden and exit when saved
                "-o", file_path.stem
            ],
            cwd=file_path.parent,
            check=True
        )

        # replace the Z:\bla\bla paths to /bla/bla unix paths, if on a unix system.
        # This is needed simply due to how d2vsource loads the video files. On linux it doesn't use wine,
        # so Z:\ paths obviously won't exist.
        if is_unix:
            with open(d2v_path, "rt", encoding="utf8") as f:
                d2v_content = f.read().splitlines()
            d2v_content = [(x[2:].replace("\\", "/") if x.startswith("Z:\\") else x) for x in d2v_content]
            with open(d2v_path, "wt", encoding="utf8") as f:
                f.write("\n".join(d2v_content))

        return d2v_path
