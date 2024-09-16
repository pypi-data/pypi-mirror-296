# video2story

**video2story** is a Python tool that allows you to convert and upload videos to your Telegram stories. It automatically cuts the video into segments and uploads them to your Telegram account.

## Installation

```bash
pip install video2story
```

## Usage

### 1. Process the video

Split the video into segments.

```bash
video2story video input.mp4 output_dir/
```

Replace `input.mp4` with the path to your video file and `output_dir/` with the directory where you want to save the processed segments. By default, the video will be cut into 60-second segments. To change that, use the `-d` option and specify the duration in seconds:

### 2. Upload the processed video

Upload the video segments to your Telegram account.

```bash
video2story story PHONE_NUMBER output_dir/ -p friends
```

Replace `PHONE_NUMBER` with your Telegram phone number and `output_dir/` with the directory containing the processed video segments. The `-p` option allows you to choose the privacy level for your story. For more options and detailed information, use the `--help` flag.

## License

This project is licensed under the GPL (GNU General Public License). See the [LICENSE](/LICENSE) file for more details.
