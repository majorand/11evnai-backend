from moviepy.editor import VideoFileClip
from io import BytesIO

def trim_video(video_bytes: bytes, start: float, end: float):
    clip = VideoFileClip(BytesIO(video_bytes))
    trimmed = clip.subclip(start, end)

    output = BytesIO()
    trimmed.write_videofile("temp.mp4", codec="libx264")
    
    with open("temp.mp4", "rb") as f:
        output.write(f.read())

    output.seek(0)
    return output


def resize_video(video_bytes: bytes, width: int):
    clip = VideoFileClip(BytesIO(video_bytes))
    resized = clip.resize(width=width)

    output = BytesIO()
    resized.write_videofile("temp.mp4", codec="libx264")

    with open("temp.mp4", "rb") as f:
        output.write(f.read())
    
    output.seek(0)
    return output
