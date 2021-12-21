"""
MIT License

Copyright (c) 2021 Janindu Malshan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import uuid
import shutil
import logging
from telegraph import upload_file
from pyrogram import Client, filters

bot = Client(
    "Telegraph Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
Hi **{}** 👋

Send me an Image and I'll send the direct link of that!

Bot by @JaguarBots
"""


@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
    msg = START_TEXT.format(message.from_user.mention)
    await message.reply_text(msg)


@bot.on_message(filters.photo & filters.private)
async def getimage(_, message):
    tmp = os.path.join("downloads", str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    img_path = os.path.join(tmp, str(uuid.uuid4()) + ".jpg")
    m = await message.reply_text("📥 Downloading...", quote=True)
    img_path = await bot.download_media(message=message, file_name=img_path)
    await m.edit("📤 Uploading...")
    try:
        response = upload_file(img_path)
    except Exception as error:
        await m.edit(f"Oops something went wrong 🤕\n\n{error}")
        return
    await m.edit(f"https://telegra.ph{response[0]}")
    shutil.rmtree(tmp, ignore_errors=True)


bot.run()
