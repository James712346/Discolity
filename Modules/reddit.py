import builtins
import praw
from random import choice
import discord, asyncio

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

async def PictureFind(message, subreddit, type = '', postsample = limit, *extra, deletemsg=True):
    subreddit = reddit.subreddit(subreddit)
    post = choice(list(subreddit.top(limit=int(postsample)))) if type.lower() == 'top' else choice(list(subreddit.hot(limit=int(postsample)))) if type.lower() == 'hot' else choice(list(subreddit.controversial(limit=int(postsample)))) if 'controversial' == type.lower() else choice(list(subreddit.new(limit=int(postsample))))
    await builtins.Tools["webhook"](message.channel, post.title, post.url, subreddit.display_name.title(), subreddit.icon_img, "https://www.reddit.com" + post.permalink, {'Upvotes': str(post.score) + " - " + str(int(post.upvote_ratio * 100)) + "%", "Comments":post.num_comments, "Flair":post.link_flair_text}, "found at https://reddit.com/r/"+ subreddit.display_name + "\nby user https://www.reddit.com/user/" + post.author.name)
    if deletemsg:
        await message.delete()

async def __init__():
    builtins.commands.update( {"reddit":PictureFind} )
    await builtins.client.loop.create_task(scheduleSend())
