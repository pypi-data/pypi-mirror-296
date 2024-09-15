from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import normpath

from video2story import cut, upload

parser = ArgumentParser(
    prog="video2story",
    description="Simple telegram story uploader",
    formatter_class=RawTextHelpFormatter,
)
subparsers = parser.add_subparsers(
    metavar="MODULE",
    dest="module",
    required=True,
)

video_parser = subparsers.add_parser(
    "video",
    help="Video processing module",
    formatter_class=RawTextHelpFormatter,
)

video_parser.add_argument(
    "filename",
    type=str,
    metavar="FILE",
    help="Video file name",
)
video_parser.add_argument(
    "output",
    type=str,
    metavar="PATH",
    help="Output folder for processed videos",
)
video_parser.add_argument(
    "-d",
    "--duration",
    type=int,
    metavar="SECONDS",
    default=60,
    help=(
        "Specifies each story duration.\n"
        "Max value is 60 and min value is 1.\n"
        "Default is 60."
    ),
)
video_parser.add_argument(
    "--no-sound",
    action="store_true",
    help="Remove sound from video.",
)
video_parser.add_argument(
    "-s",
    "--start",
    type=int,
    metavar="SECONDS",
    default=None,
    help="Specifies the second of the video from which processing will begin.",
)
video_parser.add_argument(
    "-e",
    "--end",
    type=int,
    metavar="SECONDS",
    default=None,
    help="Specifies the second of the video from which processing will end.",
)

story_parser = subparsers.add_parser(
    "story",
    help="Story publishing module",
    formatter_class=RawTextHelpFormatter,
)

story_parser.add_argument(
    "phone",
    type=str,
    metavar="PHONE",
    help="Your phone number.",
)
story_parser.add_argument(
    "input",
    type=str,
    metavar="PATH",
    help="Input folder with processed videos",
)
story_parser.add_argument(
    "-p",
    "--privacy",
    type=str,
    metavar="PRIVACY-MODE",
    choices=["everyone", "contacts", "selected", "friends"],
    default="everyone",
    help=(
        "Specifies who can see you story.\n"
        "Accept values: `everyone`, `contacts`, `selected` and `friends`.\n"
        "\n"
        "If set to `everyone` or `contacts`, the --user flag excludes the user who can see your story.\n"
        "If set to `selected`, the --user flag specifies the user who can see your story.\n"
        "If set to `friends`, the --user flag will have no effect.\n"
    ),
)
story_parser.add_argument(
    "-u",
    "--users",
    type=str,
    metavar="USERS",
    nargs="+",
    help=(
        "Behavior depends on privacy mode. See `privacy` description.\n"
        "You can specify a username or user id."
    ),
)
story_parser.add_argument(
    "-a",
    "--active-period",
    type=str,
    metavar="PERIOD",
    choices=["6h", "12h", "24h", "48h"],
    default="24h",
    help=(
        "Period after which the story is moved to archive.\n"
        "Accept values: `6h`, `12h`, `24h` and `48h`.\n"
        "Default is 24h."
    ),
)
story_parser.add_argument(
    "--save-to-profile",
    action="store_true",
    help="Keep the story accessible after expiration.",
)
story_parser.add_argument(
    "--protected-content",
    action="store_true",
    help="Protect story from forwarding and screenshotting.",
)
story_parser.add_argument(
    "--tdlib",
    type=str,
    metavar="PATH",
    help="Path to tdlib library file.",
)
story_parser.add_argument(
    "-s",
    "--start",
    type=int,
    metavar="VIDEO-ID",
    default=0,
    help=(
        "Specifies the start point of the publication.\n"
        "VIDEO-ID is the number in the name of processed file.\n"
        "Default is 0."
    ),
)
story_parser.add_argument(
    "-e",
    "--end",
    type=int,
    metavar="VIDEO-ID",
    default=None,
    help=(
        "Specifies the end point of the publication.\n"
        "VIDEO-ID is the number in the name of processed file."
    ),
)


args = parser.parse_args()
if args.module == "video":
    if not (1 <= args.duration <= 60):
        print("Duration must be between 1 and 60")
        exit(1)

    cut(
        normpath(args.filename),
        normpath(args.output),
        args.duration,
        args.no_sound,
        args.start,
        args.end,
    )
elif args.module == "story":
    upload(
        args.phone,
        normpath(args.input),
        args.privacy,
        args.users,
        args.active_period,
        args.save_to_profile,
        args.protected_content,
        args.tdlib,
        args.start,
        args.end,
    )
