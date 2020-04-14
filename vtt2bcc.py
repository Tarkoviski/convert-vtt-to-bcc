# -*- coding: utf-8 -*-
import json
import re
import sys
import os


def convertTime(time):
    hh, mm, ss = time.split(':')

    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def convertFile(filename):
    f = open(file=filename, mode="r", encoding="utf8")

    bcc_name = filename.replace(".vtt", ".bcc")
    bcc_content = {
        "font_size": 0.4,
        "font_color": "#FFFFFF",
        "background_alpha": 0.5,
        "background_color": "#9C27B0",
        "Stroke": "none",
        "body": []
    }

    matches = re.compile(
        r"((\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3}))\s+(.+)").findall(f.read())

    for match in matches:
        bcc_content["body"].append(
            {
                "from": convertTime(match[1]),
                "to": convertTime(match[2]),
                "location": 2,
                "content": match[3]
            }
        )

    bcc_file = open(bcc_name, "w", encoding="utf8")
    bcc_file.write(json.dumps(bcc_content, indent=4))

    print(
        f"Done converting {filename} to {bcc_name}!"
    )


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Running with no files nor folders specified, looking for valid files in the /subtitles foldier...")

        if os.path.isdir("subtitles"):
            for file in os.listdir("subtitles"):
                if file.endswith(".vtt"):
                    print(f"Converting subtitles/{file}...")

                    convertFile(f"subtitles/{file}")
        else:
            print("/subtitles directory not found.")
    else:
        if sys.argv[1] == "-f" and len(sys.argv) == 3:
            if os.path.isdir(sys.argv[2]):
                print(
                    f"Looking for subtitles in the {sys.argv[2]} directory...")

                for file in os.listdir(sys.argv[2]):
                    if file.endswith(".vtt"):
                        print(f"Converting {sys.argv[1]}/{sys.argv[2]}...")

                        convertFile(f"{sys.argv[2]}/{file}")
            elif os.path.isfile(sys.argv[2]) and sys.argv[2].endswith(".vtt"):
                print(f"Converting {sys.argv[2]}...")

                convertFile(sys.argv[2])
            else:
                print(
                    f"Failed. {sys.argv[2]} is not a valid .vtt file or directory.")
        else:
            if sys.argv[1] == "-f":
                print(
                    "Failed. You must specify a file or directory when using the option -f.")
            else:
                print(
                    "Failed. Invalid argument.")
