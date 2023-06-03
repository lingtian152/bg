import discord
from discord.ext import commands

import aiohttp
import asyncio
import io
import datetime
import json
import requests
import time

from config import headers
from config import number

from config import get_prefix
from config import send_anime_image
from config import TOKEN

intent = discord.Intents.default()
intent.message_content = True

client = commands.Bot(command_prefix=get_prefix, intents=intent)


def main():

    @client.event
    async def on_ready():  # 监听登录
        print("Success logged into {}".format(client.user))  # 输出登录信息
        await client.change_presence(activity=discord.Game(name='Watching Pixiv Image'))

    @client.event
    async def on_guild_join(guild):  # 监听服务器加入
        with open('server.json', 'r') as f:
            servers = json.load(f)
        # Add the server id and prefix to the dictionary
        servers[str(guild.id)] = {"id": str(guild.id), "prefix": "."}
        with open('server.json', 'w') as f:
            json.dump(servers, f, indent=4)

    @client.event
    async def on_guild_remove(guild):  # 监听服务器退出
        with open('server.json', 'r') as f:
            servers = json.load(f)
        # Remove the server id from the dictionary
        servers.pop(str(guild.id), None)
        with open('server.json', 'w') as f:
            json.dump(servers, f, indent=4)

    client.add_command(cos)
    client.add_command(pixiv)
    client.add_command(anime)
    client.add_command(prefix)
    client.add_command(骚话)
    client.add_command(騷話)
    client.add_command(ping)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(asyncio.sleep(.25))
    loop.close()

    client.run(TOKEN)  # 机器人登录


@commands.command(name="anime")
async def anime(ctx, tag=None, nsfw=None):  # 发送二次元图
    if tag == "" or tag is None:  # 检测tag
        await ctx.reply("Please specify both the anime tag.")
        return
    else:
        # 18+
        nsfw_url = f"https://api.lolicon.app/setu/v2?size=original&r18=1&tag={tag}"
        # 非18
        none_nsfw_url = f"https://api.lolicon.app/setu/v2?size=original&r18=0&tag={tag}"
        # 检测 18+消息
        if nsfw == "是" or nsfw == "yes":
            if ctx.channel.is_nsfw():
                if ctx.channel.is_nsfw():
                    print(
                        f'{datetime.datetime.now()} {ctx.author.name}: {ctx.message.content}')
                    await send_anime_image(ctx, url=nsfw_url)  # 发送消息
                    return
            else:
                await ctx.reply("This is not a NSFW channel.")
                return
        elif nsfw == "否" or nsfw is None or nsfw == "" or nsfw == "no":
            print(
                f'{datetime.datetime.now()} {ctx.author.name}: {ctx.message.content}')

            await send_anime_image(ctx, url=none_nsfw_url)  # 发送消息
            return


@commands.command(name="ping")
async def ping(ctx):
    await ctx.reply(f"Pong! {round(client.latency * 1000)}ms")


@commands.command(name="cos")
async def cos(ctx):
    ero_url = "https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=47&gids=5&is_good=true&is_hot=false&page_size=50&sort_type=1"
    try:
        print(f'{datetime.datetime.now()} {ctx.author.name}: {ctx.message.content}')
        async with aiohttp.ClientSession() as session:
            async with session.get(ero_url) as r:
                start_time = time.time()
                if r.status == 200:
                    ret = await r.json()
                    pic_url = ret["data"]["list"][number(
                        0, 39)]["post"]["cover"]
                    async with session.get(pic_url) as r:
                        pic = await r.read()
                    with io.BytesIO(pic) as file:
                        print(
                            f"Time: {datetime.datetime.now()} User: {ctx.author.name}: {pic_url}")
                        end_time = time.time()
                        print(end_time - start_time)
                        await ctx.channel.send(file=discord.File(file, "image.png"))
                        return
    except Exception as Err:
        await ctx.reply(f"There has a Error {Err}")
        print(f'错误 {Err}')
        return


@commands.command(name="pixiv")
async def pixiv(ctx, tag=None):  # 发送pixiv图
    if tag == None or tag == "":
        await ctx.reply("Please specify both the image tag.")
        return
    else:
        print(f'{datetime.datetime.now()} {ctx.author.name}: {ctx.message.content}')
        async with aiohttp.ClientSession() as session:
            url = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date_d&mode=all&p={number(0, 5)}&s_mode=s_tag'
            print(url)

            try:
                async with session.get(url, headers=headers) as response:
                    json_data = await response.json()
                    data = json_data["body"]["illustManga"]["data"]

                    for _ in range(70):  # Try up to 70 times
                        num = number(0, len(data)-1)  # Get a random index
                        # Get the artwork at the random index
                        artwork = data[num]

                        # Check if the artwork is not AI-generated
                        if 'aiType' in artwork and artwork['aiType'] != 1:
                            pic_id = artwork["id"]  # Get the picture ID

                            # Download the picture
                            download_url = f"https://www.pixiv.cat/{pic_id}.jpg"
                            async with session.get(download_url) as f:
                                image_data = await f.read()  # Read the content of the response

                            # Use the content to create a file-like object
                            with io.BytesIO(image_data) as file:
                                print(
                                    f"Time: {datetime.datetime.now()} User: {ctx.author.name}: {f}")
                                await asyncio.sleep(0.25)
                                # Send the picture
                                await ctx.channel.send(file=discord.File(file, "image.jpg"))
                                return  # Exit the function after sending the image
            except Exception as Err:
                await ctx.reply(f"There has a Error " + f"{Err}")
                return


@commands.command(name="骚话")
async def 骚话(ctx):
    try:
        print(f'{datetime.datetime.now()} {ctx.author.name}: {ctx.message.content}')
        req = requests.get("http://api.ay15.cn/api/saohua/api.php")
        text = req.content

        await ctx.reply(text.decode("utf-8"))
        return
    except Exception as Err:
        await ctx.reply(f"There has a Error {Err}")
        print(f'错误 {Err}')
        return


@commands.command(name="騷話")
async def 騷話(ctx):
    try:
        print(f'{datetime.datetime.now()} {ctx.author.name}: {ctx.message.content}')
        req = requests.get("http://api.ay15.cn/api/saohua/api.php")
        text = req.content

        await ctx.reply(text.decode("utf-8"))
        return
    except Exception as Err:
        await ctx.reply(f"There has a Error {Err}")
        print(f'错误 {Err}')
        return


@commands.command(name="prefix")
async def prefix(ctx, prefix=None):
    if prefix == None or prefix == "":
        await ctx.reply(f"Please specify the prefix.")
        return
    else:
        with open('server.json', 'r') as f:
            servers = json.load(f)

        servers[str(ctx.guild.id)]["prefix"] = prefix

        with open('server.json', 'w') as f:
            json.dump(servers, f, indent=4)
        await ctx.reply(f"Prefix changed to {prefix}")


if __name__ == "__main__":
    asyncio.run(main())
