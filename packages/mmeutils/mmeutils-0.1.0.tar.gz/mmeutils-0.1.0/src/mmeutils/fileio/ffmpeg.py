"""FFmpeg Launcher Module"""


import shutil
import subprocess

from typing import List


def get_ffmpeg_bin(ignore_local: bool=False) -> str:
    """Returns the full path to an `ffmpeg` binary.

    If no `ffmpeg` binary can be found locally `pyffmpeg` will be used
    (which downloads a local copy into the user profile).

    :param ignore_local: Do not use/search local `ffmpeg` copies
        (excludes `pyffmpeg`)
    :type ignore_local: bool

    :return: The full path to an `ffmpeg` binary.
    :rtype: str
    """
    ffmpeg_bin = None

    if not ignore_local:
        ffmpeg_bin = shutil.which("ffmpeg")

    if ffmpeg_bin is None:
        from pyffmpeg import FFmpeg
        ffmpeg = FFmpeg(enable_log=False)
        ffmpeg_bin = ffmpeg.get_ffmpeg_bin()

    return ffmpeg_bin


def run_ffmpeg(args: List[str]) -> bool:
    """Locates and runs an `ffmpeg` binary with supplied arguments.

    :param args: The arguments for `ffmpeg`.
    :type args: List[str]

    :return: True on success, False on error.
    :rtype: bool
    """
    proc_args = [get_ffmpeg_bin()]

    proc_args += args

    result = subprocess.run(
        proc_args,
        encoding='utf-8',
        capture_output=True,
        check=True,
    )

    return result.returncode == 0
