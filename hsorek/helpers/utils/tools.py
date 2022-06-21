import os
from typing import Optional

from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import edit_or_reply
from ..tools import media_type
from .utils import runcmd

LOGS = logging.getLogger(__name__)


async def media_to_pic(event, reply, noedits=False):  # sourcery no-metrics
    mediatype = media_type(reply)
    if mediatype not in [
        "Photo",
        "Round Video",
        "Gif",
        "Sticker",
        "Video",
        "Voice",
        "Audio",
        "Document",
    ]:
        return event, None
    if not noedits:
        hsorekevent = await edit_or_reply(
            event, "**⎙ :: جاري التحويل انتظر قليلا  ** ...."
        )

    else:
        hsorekevent = event
    hsorekmedia = None
    hsorekfile = os.path.join("./temp/", "meme.png")
    if os.path.exists(hsorekfile):
        os.remove(hsorekfile)
    if mediatype == "Photo":
        hsorekmedia = await reply.download_media(file="./temp")
        im = Image.open(hsorekmedia)
        im.save(hsorekfile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, hsorekfile, thumb=-1)
    elif mediatype == "Sticker":
        hsorekmedia = await reply.download_media(file="./temp")
        if hsorekmedia.endswith(".tgs"):
            hsorekcmd = f"lottie_convert.py --frame 0 -if lottie -of png '{hsorekmedia}' '{hsorekfile}'"
            stdout, stderr = (await runcmd(hsorekcmd))[:2]
            if stderr:
                LOGS.info(stdout + stderr)
        elif hsorekmedia.endswith(".webp"):
            im = Image.open(hsorekmedia)
            im.save(hsorekfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, hsorekfile, thumb=-1)
        if not os.path.exists(hsorekfile):
            hsorekmedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(hsorekfile, 0.1)
            except Exception:
                clip = clip.save_frame(hsorekfile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            hsorekmedia = await reply.download_media(file="./temp")
            im = Image.open(hsorekmedia)
            im.save(hsorekfile)
    if hsorekmedia and os.path.lexists(hsorekmedia):
        os.remove(hsorekmedia)
    if os.path.lexists(hsorekfile):
        return hsorekevent, hsorekfile, mediatype
    return hsorekevent, None


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
