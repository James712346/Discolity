import builtins, discord, traceback, json, asyncio, os, Log
from subprocess import Popen, PIPE

#-- Module Start --#
if not 'msgtimeout' in builtins.config["MAIN"]:
     builtins.config["MAIN"]['msgtimeout'] = '20'
     with open('config.ini', 'w') as configfile:
         builtins.config.write(configfile)

if not 'Fallback_Option' in builtins.config:
    builtins.config["Fallback_Option"] = dict(streamable_email="", streamable_pass='')
    with open('config.ini', 'w') as configfile:
        builtins.config.write(configfile)

DELAY = int(builtins.config["MAIN"]['msgtimeout'])


async def error(mobject, errorType, errorDesc, *extras):
    embed = discord.Embed(
        title=errorType, description=errorDesc, color=0xff0000)
    embed.set_thumbnail(
        url="https://cdn.clipart.email/530a9899f5c308ce5a719a217d1500ca_redx-clip-art-at-clkercom-vector-clip-art-online-royalty-free-_504-598.png")
    for extra in extras:
        embed.add_field(name=extra[0], value=extra[1])
    embed.set_footer(text="this isn't very fat joe")
    errormessage = await mobject.channel.send(embed=embed)
    await errormessage.delete(delay=DELAY)
    await mobject.delete(delay=DELAY)


async def response(mobject, responseType, responsiveDesc, *extras):
    embed = discord.Embed(
        title=responseType, description=responsiveDesc, color=0x3F88C5)
    embed.set_thumbnail(
        url="https://lesspestcontrol.com.au/wp-content/uploads/green-tick.png")
    for extra in extras:
        embed.add_field(name=extra[0], value=extra[1])
    embed.set_footer(text="This is quite mumbai!")
    responsemessage = await mobject.channel.send(embed=embed)
    await responsemessage.delete(delay=DELAY + 10)
    await mobject.delete(delay=DELAY + 10)

async def webhook(channel, title, url, name="Equality", avatar_url="", embed_url="", variables = {}, footer = '', description='', savesAllowed=False):
    webhook = await channel.create_webhook(name=name)
    embed = discord.Embed(title=title, url=embed_url, description=description+'\n'+embed_url)
    for variable in variables:
        embed.add_field(name=variable, value=variables[variable],inline=True)
    embed.set_footer(text=footer + "\nDone by Discolity"+ ("\nReact with the 💾 icon to save this post" if savesAllowed else ""))
    if ('.jpg' in url or '.png' in url or '.gif' in url) and not 'temp/' in url:
        url = url.replace('gifv','gif') if '.gifv' in url else url
        embed.set_image(url=url)
        url = ""
    if 'temp/' in url:
        conv = await channel.send("Send File")
        Openfile = open(url,'rb')
        if channel.guild.filesize_limit > os.fstat(Openfile.fileno()).st_size:
            await webhook.send(username=name,avatar_url=avatar_url,embed=embed, file=discord.File(Openfile))
        else:
            Log.Verbose("Failed to upload, file is too big, using fallback")
            returned = Popen("curl https://api.streamable.com/upload -u "+builtins.config["Fallback_Option"]["streamable_email"]+":"+builtins.config["Fallback_Option"]["streamable_pass"]+" -F file=@"+url,stdout=PIPE)
            loading = ['|', '//', '-', '\\']
            pointer = 0
            while returned.poll() is None:
                await conv.edit(content = "Sending File " + loading[pointer])
                if pointer == 3:
                    pointer = 0
                else:
                    pointer+=1
                await asyncio.sleep(0.5)
            out, erro = returned.communicate()
            await webhook.send('https://streamable.com/' + json.loads(out)['shortcode'])
            await webhook.send(username=name,avatar_url=avatar_url,embed=embed)
        Openfile.close()
        await conv.delete()
        await webhook.delete()
        return
    if url:
        await webhook.send(url)
    await webhook.send(username=name,avatar_url=avatar_url,embed=embed)
    await webhook.delete()


async def process_command(message):
    if message.content.startswith(builtins.config["MAIN"]["defualtcommandsymbol"]) and not message.author.bot :
        try:
            fixcontent = message.content
            for mention in message.mentions:
                fixcontent = fixcontent.replace(
                    "<@!" + str(mention.id) + ">", "")
            for mention in message.role_mentions:
                fixcontent = fixcontent.replace(
                    "<@&" + str(mention.id) + ">", "")
            for mention in message.channel_mentions:
                fixcontent = fixcontent.replace(
                    "<#" + str(mention.id) + ">", "")
            command = message.content[len(builtins.config["MAIN"]["defualtcommandsymbol"]):].split()[0].lower()
            args = fixcontent[len(builtins.config["MAIN"]["defualtcommandsymbol"]):].split()[1:]
            if command in builtins.commands.keys():
                Log.Verbose("Processing", command, "command")
                await builtins.commands[command](message, *args)
                Log.Verbose("Finished running",command)
            else:
                await error(message, "Command Error", "Either this command doesn't exist or the module hasn't been loaded", ["Command Inputted", command])
        except Exception as e:
            Log.Error(traceback.format_exc())
            await error(message, "Command Error", "Either the Module Errored out all there is incorrect charaters in you command, **Console OutPut is Below v** \n ```bash\n" + traceback.format_exc() + "\n```")

async def __init__():
    builtins.events["on_message"].append( process_command )
    builtins.Tools.update( { "errormsg": error, "responsemsg": response, "webhook": webhook } )
    Log.Verbose("Message has started")
