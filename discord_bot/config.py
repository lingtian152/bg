import random
import json
import aiohttp
import io
import datetime
import asyncio
import discord

TOKEN = "MTA4NTc1OTA0NjM3MzYyNTg3Ng.Gk09mI.J9N42uVPiNcXUoDIMWA_Bia2UTds7DBo2SsUWo"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
           'Cache-Control': 'no-cache',
           }


def number(x, y):
    num = random.randint(x, y)
    return num


def get_prefix(client, message):
    with open('server.json', 'r') as f:
        servers = json.load(f)

    return servers[str(message.guild.id)]["prefix"]


async def send_anime_image(ctx, url=None):  # 发送图片函数
    if url is None:
        return
    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as r:
                    ret = await r.json()
                    await asyncio.sleep(0.25)
                    pic_url = ret["data"][0]["urls"]["original"]
                    async with session.get(pic_url) as r:
                        if r.status != 200:
                            await ctx.reply("This page has some error, send message failure, please retry again")
                        elif r.status == 200:
                            img = await r.read()  # reads image from response
            with io.BytesIO(img) as file:  # converts to file-like object
                print(
                    f"Time: {datetime.datetime.now()} User: {ctx.author.name}: {pic_url}")
                await asyncio.sleep(1)
                return await ctx.channel.send(f"{ctx.author.mention}", file=discord.File(file, "image.png"))
        except aiohttp.ClientResponseError as e:
            await ctx.reply(f"There has a Error {e}")
        except IndexError as e:
            await ctx.send(f'An error occurred while processing the data: {e}')
        except Exception as e:
            return await ctx.reply(f"There has a Error {e}")
