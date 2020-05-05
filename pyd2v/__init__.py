class D2V:
    """
    Object containing information on D2V Project Files
    """
    def __init__(self, filename):
        """
        Parse a d2v file
        :param str filename: path to the d2v file to be parsed
        :rtype: :class:`D2V`.
        :raises ValueError: if parsing fails
        """
        # Header
        self.version = None
        self.videos = None
        # Settings
        self.settings = None
        # Data
        self.data = None
        self.data_type = None
        with open(filename, mode="r", encoding="utf-8") as f:
            # Version
            self.version = f.readline().strip()
            if not self.version.startswith("DGIndexProjectFile"):
                raise ValueError(f"Expected Version Header, received:\n\t{self.version}")
            self.version = self.version[18:]  # strip "DGIndexProjectFile"
            # Videos
            self.videos = []
            for n in range(int(f.readline().strip())):
                self.videos.append(f.readline().strip())
            # Headers Terminate Check
            if len(f.readline().strip()) > 0:
                raise ValueError("Unexpected data after reading Header's Video List.")
            # Settings
            self.settings = {}
            int_list = ["Stream_Type", "MPEG_Type", "iDCT_Algorithm", "YUVRGB_Scale", "Field_Operation"]
            while True:
                line = f.readline().strip()
                # Settings Terminate Check
                if len(line) == 0:
                    break
                line = line.split("=", maxsplit=2)
                self.settings[line[0]] = int(line[1]) if line[0] in int_list else line[1]
            if self.settings["Stream_Type"] == 2:
                self.settings["MPEG2_Transport_PID"] = self.settings["MPEG2_Transport_PID"].split(",")
                self.settings["MPEG2_Transport_PID"] = {
                    "Video": float(self.settings["MPEG2_Transport_PID"][0]),
                    "Audio": float(self.settings["MPEG2_Transport_PID"][1]),
                    "PCR": float(self.settings["MPEG2_Transport_PID"][2])
                }
                self.settings["Transport_Packet_Size"] = self.settings["Transport_Packet_Size"].split(",")
            self.settings["Luminance_Filter"] = self.settings["Luminance_Filter"].split(",")
            self.settings["Luminance_Filter"] = {
                "Gamma": float(self.settings["Luminance_Filter"][0]),
                "Offset": float(self.settings["Luminance_Filter"][1])
            }
            self.settings["Clipping"] = [int(x) for x in self.settings["Clipping"].split(",")]
            if "," in self.settings["Aspect_Ratio"]:
                self.settings["Aspect_Ratio"] = [
                    (x if ":" in x else float(x)) for x in self.settings["Aspect_Ratio"].split(",")
                ]
            elif ":" not in self.settings["Aspect_Ratio"]:
                self.settings["Aspect_Ratio"] = float(self.settings["Aspect_Ratio"])
            self.settings["Picture_Size"] = [int(x) for x in self.settings["Picture_Size"].split("x")]
            self.settings["Frame_Rate"] = self.settings["Frame_Rate"].split(" ")
            self.settings["Frame_Rate"] = [
                self.settings["Frame_Rate"][0],
                [int(x) for x in self.settings["Frame_Rate"][1].strip("()").split("/")]
            ]
            self.settings["Location"] = self.settings["Location"].split(",")
            self.settings["Location"] = {
                "StartFile": self.settings["Location"][0],
                "StartOffset": self.settings["Location"][1],
                "EndFile": self.settings["Location"][2],
                "EndOffset": self.settings["Location"][3]
            }
            # Data
            self.data = []
            while True:
                line = f.readline().strip()
                # Data Terminate Check
                if len(line) == 0:
                    break
                line = line.split(" ", maxsplit=7)
                data = {
                    "info": bin(int(line[0], 16))[2:].zfill(8),
                    "matrix": line[1],
                    "file": line[2],
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
