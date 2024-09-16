from os import makedirs
from os.path import exists, isdir, join
from subprocess import Popen


def cut(
    filename: str,
    output_dir: str,
    duration: int,
    no_sound: bool,
    start: int | None,
    end: int | None,
) -> None:
    if not exists(output_dir):
        makedirs(output_dir)
    elif not isdir(output_dir):
        print("Output is not a directory")
        exit(1)
    process = Popen(
        [
            "ffmpeg",
            "-y",
            # Input file
            *("-i", filename),
            # Start point
            *(("-ss", str(start)) if start is not None else ()),
            # End point
            *(("-to", str(end)) if end is not None else ()),
            # Codec
            *("-c:v", "libx264"),
            *(("-an",) if no_sound else ("-c:a", "mp3")),
            # Video centring
            *(
                "-vf",
                "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:-1:-1,setsar=1",
            ),
            # Segment splitter
            *("-f", "segment"),
            *("-segment_time", str(duration)),
            *("-reset_timestamps", "1"),
            *("-force_key_frames", f"expr:gte(t,n_forced*{duration})"),
            # Output
            join(output_dir, "%d.mp4"),
        ]
    )

    exit_code = process.wait()
    if exit_code != 0:
        exit(exit_code)
