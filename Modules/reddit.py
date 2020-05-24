import builtins
import praw
from random import choice
import discord, asyncio
from urllib.request import urlretrieve
import ffmpy, os, time, re

async def tempdelete():
    while not builtins.client.is_closed():
        print("Logging | Clearing out Temp File")
        for filename in os.listdir("temp/"):
            file_time = os.path.getmtime("temp/"+filename)
            if (time.time() - file_time) / 60 > 5:
                print("Deleting", filename)
                os.remove("temp/"+filename)
            else:
                return False
        print("Logging | Done")
        await asyncio.sleep(300) # task runs every 30 minutes

async def scheduleSend():
    while not builtins.client.is_closed():
        for guild in builtins.client.guilds:
            channel = discord.utils.get(guild.text_channels, name='reddit')
            if channel:
                subreddit = reddit.subreddit('nsfw')
                post = choice(list(subreddit.new(limit=limit)))
                await builtins.Tools["webhook"](channel, post.title, post.url, subreddit.display_name, subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name)
        await asyncio.sleep(1800) # task runs every 30 minutes

if not 'reddit' in builtins.config:
    builtins.config["reddit"] = dict(client_id='',client_secret='',user_agent='',username='',password='',postsample=20)
    with open('config.ini', 'w') as configfile:
        builtins.config.write(configfile)

send = dict(builtins.config["reddit"])
limit = int(send.pop('postsample'))
reddit = praw.Reddit(**send)

async def converturl(post):
    if "v.redd" in post.url:
        videourl = post.media["reddit_video"]["fallback_url"]
        videourl = videourl.split("?")[0]
        audiourl = post.url + '/audio'
        post.url = "temp/" + post.title[:30].rstrip().replace(" ","_") + ".mp4"
        urlretrieve(videourl, post.url)
        if post.media["reddit_video"]["is_gif"]:
            old_url = post.url
            post.url = "temp/" + post.title[:30].rstrip().replace(" ","_") + ".gif"
            ff = ffmpy.FFmpeg( global_options= "-loglevel 0 -hide_banner -nostats -y",
            	inputs = {old_url : None},
            	outputs = {post.url : None})
            ff.run()
        else:
            try:
                audiopath = "temp/" + post.title[:30].rstrip().replace(" ","_") + ".mp3"
                videoaudio = "temp/" + post.title[:30].rstrip().replace(" ","_") + "-Audio.mp4"
                urlretrieve(audiourl, audiopath)
                os.system('ffmpeg -hide_banner -loglevel panic -y -i '+ post.url +' -i '+ audiopath +' -vcodec copy -acodec copy '+videoaudio)
                post.url = videoaudio
            except:
                pass


async def PictureFind(message, subreddit, type = '', postsample = limit, *extra, deletemsg=True):
    subreddit = reddit.subreddit(subreddit)
    post = choice(list(subreddit.top(limit=int(postsample)))) if type.lower() == 'top' else choice(list(subreddit.hot(limit=int(postsample)))) if type.lower() == 'hot' else choice(list(subreddit.controversial(limit=int(postsample)))) if 'controversial' == type.lower() else choice(list(subreddit.new(limit=int(postsample))))
    await converturl(post)
    await builtins.Tools["webhook"](message.channel, post.title, post.url, subreddit.display_name.title(), subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found by "+ message.author.display_name +" at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name)
    if deletemsg:
        await message.delete()

async def formatreddit(message, url, *extra, comment):
    post = reddit.submission(url=url)
    subreddit = post.subreddit
    print(post.media)
    await converturl(post)
    await builtins.Tools["webhook"](message.channel, post.title, post.url, subreddit.display_name.title(), subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found by "+ message.author.display_name +" at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name, comment)
    await message.delete()

async def isRedditurl(message):
    try:
        url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
        if (not (message.author.bot or message.content.startswith(builtins.config["MAIN"]["defualtcommandsymbol"]))) and "reddit.com/r/" in url and '/comments/' in url:
            await formatreddit(message, url, comment=message.content.replace(url,""))
    except:
        pass

async def __init__():
    builtins.commands.update( {"reddit":PictureFind, "freddit":formatreddit} )
    builtins.events["on_message"].append( isRedditurl )
    await builtins.client.loop.create_task(tempdelete())
    await builtins.client.loop.create_task(scheduleSend())
