# JupyterVideo

Worry-free inline videos in Jupyter Notebooks that stay.

## Installation

```bash
pip install jupytervideo
```

## Usage

```python
from jupytervideo import JupyterVideo


video = JupyterVideo("path/to/video.mp4")


for _ in range(10):
    # frame = ...  Get a frame from somewhere

    video.write(frame)

video.show()

# The video will be displayed inline in the notebook
```

## Why?

Jupyter Notebooks support displaying videos inline using HTML5 video tags. However, the videos are embedded as base64 strings, which can make the notebook size very large. Using compressed short video files
is less likely to bloat the notebook size, but when generating videos frame by frame (e.g. in a simulation, or with opencv), the video is not compressed optimally. This package aims to provide a simple way to generate videos frame by frame, compress them with `ffmpeg`, and display them inline in Jupyter Notebooks.

## How?

The `JupyterVideo` class writes frames to a temporary directory, and when the video is displayed, it compresses the video using `ffmpeg` and displays it inline in the notebook.

## Requirements

- `ffmpeg` must be installed and available in the system path.

## License

MIT