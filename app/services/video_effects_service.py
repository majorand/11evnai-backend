from moviepy.editor import VideoFileClip, vfx
from io import BytesIO

def apply_effect(video_bytes: bytes, effect: str):
    clip = VideoFileClip(BytesIO(video_bytes))

    if effect == "invert":
        processed = clip.fx(vfx.invert_colors)
    elif effect == "blackwhite":
        processed = clip.fx(vfx.blackwhite)
    elif effect == "mirror":
        processed = clip.fx(vfx.mirror_x)
    else:
        processed = clip

    output = BytesIO()
    processed.write_videofile("temp.mp4", codec="libx264")

    with open("temp.mp4", "rb") as f:
        output.write(f.read())

    output.seek(0)
    return output
