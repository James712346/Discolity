import builtins
import praw
from random import choice
import discord, asyncio
from urllib.request import urlretrieve
import ffmpy, os, time, re

Regex = r'(?P<url>https?://(?:[^/]+\.)?reddit\.com/r/[^/]+/comments/(?P<id>[^/?#&]+))'
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
        await asyncio.sleep(900) # task runs every 10 minutes

async def scheduleSend():
    while not builtins.client.is_closed():
        for guild in builtins.client.guilds:
            catagory = discord.utils.get(guild.categories, name='reddit')
            if not catagory:
                catagory = await guild.create_category("reddit")
                print(catagory.name)
            else:
                for channel in catagory.text_channels:
                    async for message in channel.history(limit=1, oldest_first=True):
                        first_message = message
                    if "Subs" in first_message.content:
                        subs = choice("".join(first_message.content.split(":")[1:]).split(",")).strip()
                    else:
                        await channel.send("Subs: "+ channel.name)
                        subs = channel.name
                    try:
                        subreddit = reddit.subreddit(subs)
                        post = choice(list(subreddit.new(limit=limit)))
                        await converturl(post)
                        await builtins.Tools["webhook"](channel, post.title, post.url, subreddit.display_name, subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name)
                    except:
                        print(subs,"FAILED")
        await asyncio.sleep(900) # task runs every 15 minutes

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

async def formatreddit(message, url, *extra, comment=""):
    test = re.search(Regex, url)
    if test:
        post = reddit.submission(url=url)
        subreddit = post.subreddit
        await converturl(post)
        await builtins.Tools["webhook"](message.channel, post.title, post.url, subreddit.display_name.title(), subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found by "+ message.author.display_name +" at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name, comment)
        await message.delete()
    else:
        await builtins.Tools["errormsg"](message, "Known URL", "Please use reddit submission links eg `https://reddit.com/r/subreddit/comments/postid`",["Inputted URL",url])

async def isRedditurl(message):
    url = re.search(Regex, message.content)
    if (not (message.author.bot or message.content.startswith(builtins.config["MAIN"]["defualtcommandsymbol"]))) and url:
        await formatreddit(message, url.group(), comment=message.content.replace(url.group(),""))

async def __init__():
    builtins.commands.update( {"reddit":PictureFind, "freddit":formatreddit} )
    builtins.events["on_message"].append( isRedditurl )
    builtins.client.loop.create_task(tempdelete())
    builtins.client.loop.create_task(scheduleSend())
