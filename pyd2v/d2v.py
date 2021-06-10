from io import StringIO
from pathlib import Path
from typing import TextIO


class D2V:
    """DGIndex D2V project file."""

    def __init__(self, f: TextIO):
        """
        Parse a d2v.
        :param str f: Text IO object of a d2v to be parsed.
        :raises ValueError: if parsing fails
        """
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
    def loads(cls, data: str):
        """Parse a D2V from a blob of string data."""
        return cls(StringIO(data))

    @classmethod
    def load(cls, file: Path):
        """Parse a D2V from a file."""
        return cls(file.open(mode="r", encoding="utf8"))
