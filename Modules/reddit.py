import builtins, traceback
import praw
from random import choice
import discord, asyncio
from urllib.request import urlretrieve
import ffmpy, os, time, re, Log
Save_Channel = "saves"
Regex = r'(?P<url>https?://(?:[^/]+\.)?reddit\.com/r/[^/]+/comments/(?P<id>[^/?#&]+))'


async def tempdelete():
    while True:
        Log.Log("Scheduled clearing out temp folder")
        numfiledel = 0
        for filename in os.listdir("temp/"):
            file_time = os.path.getmtime("temp/"+filename)
            if (time.time() - file_time) / 60 > 5:
                Log.Verbose("Deleting", filename)
                os.remove("temp/"+filename)
                numfiledel += 1
        Log.Success("Finished scheduled clearing out temp folder\nFiles removed:",numfiledel)
        await asyncio.sleep(600) # task runs every 10 minutes

async def scheduleSend():
    while True:
        Log.Verbose("Scheduled Reddit Send")
        try:
            for guild in builtins.client.guilds:
                catagory = discord.utils.get(guild.categories, name='reddit')
                if not catagory:
                    catagory = await guild.create_category("reddit")
                    await catagory.create_text_channel(Save_Channel)
                    Log.Verbose("Create Category for Reddit: ",catagory.name)
                else:
                    for channel in catagory.text_channels:
                        if channel.name in [Save_Channel, Save_Channel+"-nsfw"]:
                            continue
                        async for message in channel.history(limit=1, oldest_first=True):
                            first_message = message
                        if "Subs" in first_message.content:
                            subs = "".join(first_message.content.split(":")[1:]).split(",")
                        else:
                            await channel.send("Subs: "+ channel.name)
                            subs = [channel.name]
                        try:
                            subreddit = reddit.subreddit(choice(subs).strip())
                            while not (subreddit.over18 == channel.is_nsfw() or channel.is_nsfw()):
                                await asyncio.sleep(1)
                                subreddit = reddit.subreddit(choice(subs).strip())
                            post = choice(list(subreddit.new(limit=limit)))
                            while not (post.over_18 == channel.is_nsfw() or channel.is_nsfw()):
                                await asyncio.sleep(1)
                                post = choice(list(subreddit.new(limit=limit)))
                            await converturl(post)
                            await builtins.Tools["webhook"](channel, post.title, post.url, subreddit.display_name, subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name if  post.author.name else "unknown", savesAllowed=True)
                        except Exception:
                            Log.Error("When parsing "+", ".join(subs)+"\n",traceback.format_exc())
        except Exception as e:
            Log.Error(traceback.format_exc())
            pass
        Log.Verbose("Finished Scheduled Reddit Send")
        await asyncio.sleep(900) # task runs every 15 minutes

async def savepost(reaction, user):
    if reaction.emoji == "💾" and reaction.message.channel.category.name == 'reddit':
        url = re.search(Regex,reaction.message.embeds[0].description).group()
        post = reddit.submission(url=url)
        subreddit = post.subreddit
        save_channel = Save_Channel
        if post.over_18:
            save_channel = Save_Channel + '-nsfw'
        text_channel = discord.utils.get(reaction.message.channel.category.text_channels, name=save_channel)
        if not text_channel:
            text_channel = await reaction.message.channel.category.create_text_channel(save_channel)
        await converturl(post)
        await builtins.Tools["webhook"](text_channel, post.title, post.url, subreddit.display_name.title(), subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "saved by "+ user.display_name +"\nfound at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name)
        await reaction.remove(user)
        Log.Verbose("Saved Reddit Post")

if not 'reddit' in builtins.config:
    builtins.config["reddit"] = dict(client_id='',client_secret='',user_agent='',username='',password='',postsample=20)
    with open('config.ini', 'w') as configfile:
        builtins.config.write(configfile)

send = dict(builtins.config["reddit"])
limit = int(send.pop('postsample'))
reddit = praw.Reddit(**send)

async def converturl(post):
    if "v.redd" in post.url:
        Log.Verbose("Downloading Reddit Video")
        videourl = post.media["reddit_video"]["fallback_url"]
        videourl = videourl.split("?")[0]
        audiourl = post.url + '/audio'
        post.url = "temp/" + post.title[:30].encode("ascii", errors="ignore").decode().rstrip().replace(" ","_").replace("*","") + ".mp4"
        urlretrieve(videourl, post.url)
        if post.media["reddit_video"]["is_gif"]:
            old_url = post.url
            post.url = "temp/" + post.title[:30].encode("ascii", errors="ignore").decode().rstrip().replace(" ","_") + ".gif"
            ff = ffmpy.FFmpeg( global_options= "-loglevel 0 -hide_banner -nostats -y",
            	inputs = {old_url : None},
            	outputs = {post.url : None})
            ff.run()
        else:
            try:
                audiopath = "temp/" + post.title[:30].encode("ascii", errors="ignore").decode().rstrip().replace(" ","_") + ".mp3"
                videoaudio = "temp/" + post.title[:30].encode("ascii", errors="ignore").decode().rstrip().replace(" ","_") + "-Audio.mp4"
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
    builtins.events["on_reaction_add"].append( savepost )
    builtins.client.loop.create_task(tempdelete())
    builtins.client.loop.create_task(scheduleSend())
    Log.Verbose("Reddit has started")
