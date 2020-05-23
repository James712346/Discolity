import builtins, discord, traceback

#-- Module Start --#
if not 'msgtimeout' in builtins.config["MAIN"]:
     builtins.config["MAIN"]['msgtimeout'] = '20'
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

async def webhook(channel,title, url, name="Equality", avatar_url="", embed_url="", variables = {}, footer = ''):
    webhook = await channel.create_webhook(name=name)
    embed = discord.Embed(title=title, url=embed_url, description=embed_url)
    for variable in variables:
        embed.add_field(name=variable, value=variables[variable],inline=True)
    embed.set_footer(text=footer + "    Done by Discolity")
    if '.jpg' in url or '.png' in url or '.gif' in url:
        url = url.replace('gifv','gif') if '.gifv' in url else url
        embed.set_image(url=url)
        url = ""
    await webhook.send(username=name,avatar_url=avatar_url,embed=embed)
    if url:
        await webhook.send(url)

    await webhook.delete()


async def process_command(message):
    print(message.content)
    if message.content.startswith(builtins.config["MAIN"]["defualtcommandsymbol"]) and not message.author.bot :
        try:
            print( message.content)
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
                print("Processing", command, "command")
                await builtins.commands[command](message, *args)
            else:
                await error(message, "Command Error", "Either this command doesn't exist or the module hasn't been loaded", ["Command Inputted", command])
        except Exception as e:
            await error(message, "Command Error", "Either the Module Errored out all there is incorrect charaters in you command, **Console OutPut is Below v** \n ```bash\n" + "".join(traceback.format_exception_only(e.__class__, e)) + "\n```")

async def __init__():
    builtins.events["on_message"].append( process_command )
    builtins.Tools.update( { "errormsg": error, "responsemsg": response, "webhook": webhook } )
