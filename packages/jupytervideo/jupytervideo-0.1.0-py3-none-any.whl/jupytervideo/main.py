import os
import subprocess

import cv2
from IPython.display import Video
from typing import Tuple


# Check if `ffmpeg` is installed
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE)
    except FileNotFoundError:
        raise FileNotFoundError(
            "ffmpeg not found. Please install ffmpeg first and make sure it is added to the system PATH."
        )


check_ffmpeg()


class JupyterVideo:
    """
    A class to handle video output in Jupyter notebook without hassle. It writes frames to a video file and compresses it if needed.
    Attributes:
        path (str): The file path where the video will be saved.
        width (int): The width of the video frames.
        height (int): The height of the video frames.
        compress (bool): Flag to determine if the video should be compressed.
        scale (int): The scale factor for resizing the video frames.
        video_writer (cv2.VideoWriter): The OpenCV VideoWriter object for writing frames to the video file.
    """

    def __init__(
        self,
        path: str,
        fps: int,
        size: Tuple[int, int],
        scale: int = 1,
        compress: bool = True,
    ):
        """
        Create a new VideoOutput object.
        Parameters:
            path (str): The file path where the video will be saved.
            fps (int): The frames per second of the video.
            size (tuple): The size of the video frames (width, height).
            scale (int): The scale factor for resizing the video frames.
            compress (bool): Flag to determine if the video should be compressed.
        """

        if not path.endswith(".mp4"):
            raise ValueError("The video file should be in .mp4 format.")

        if not isinstance(fps, int) or fps <= 0:
            raise ValueError("fps should be a positive integer.")

        if (
            not isinstance(size, tuple)
            or len(size) != 2
            or not all(isinstance(i, int) for i in size)
            or any(i <= 0 for i in size)
        ):
            raise ValueError("size should be a tuple of two positive integers.")

        if not isinstance(scale, int) or scale <= 0:
            raise ValueError("scale should be a positive integer.")

        if not isinstance(compress, bool):
            raise ValueError("compress should be a boolean.")

        directory = os.path.dirname(path) or "."
        if not os.path.exists(directory):
            raise FileNotFoundError("The directory to save the video does not exist.")

        self.path = path
        self.width = size[0]
        self.height = size[1]
        self.compress = compress
        self.scale = scale

        self.video_writer = cv2.VideoWriter(
            path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (self.width // self.scale, self.height // self.scale),
        )

    def write(self, frame):
        if frame.shape[:2] != (self.height, self.width):
            raise ValueError(f"Frame size should be ({self.width}, {self.height}).")

        if self.scale != 1:
            out_frame = cv2.resize(
                frame,
                (self.width // self.scale, self.height // self.scale),
                interpolation=cv2.INTER_AREA,
            )
        else:
            out_frame = frame

        self.video_writer.write(out_frame)

    def show(self):
        self.video_writer.release()

        if self.compress:
            new_path = self.path.replace(".mp4", "_compressed.mp4")
            subprocess.run(
                [
                    "ffmpeg",
                    "-nostats",
                    "-loglevel",
                    "error",
                    "-i",
                    self.path,
                    "-vcodec",
                    "libx264",
                    "-crf",
                    "30",
                    new_path,
                ],
                stdout=subprocess.PIPE,
            )

            os.remove(self.path)
            os.rename(new_path, self.path)

        return Video(
            self.path,
            embed=True,
            width=self.width // self.scale,
            height=self.height // self.scale,
        )
