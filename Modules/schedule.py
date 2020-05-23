import discord, asyncio, builtins, json


class schedule:
    async def setup(self,command, *extra, message = False, channelid = False, guildid = False, time='30m' , args = [], statusid = None):
        if message:
            channelid = message.channel.id
            guildid = message.channel.id
        format = time[-1].lower()
        self.time = int(time[:-1])
        if format in ['d']:
            self.time = self.time * 24
        if format in ['h','d','w']:
            self.time = self.time * 60
        if format in ['m','h','d','w']:
            self.time = self.time * 60
        self.command = command
        self.args = args
        self.channelid = channelid
        self.guildid = guildid
        print(self.args)
        if message:
            self.databaseformat = dict(userid=message.author.id, guildid = message.guild.id, statusid = statusid, channelid = message.channel.id, type="s", args = str(args), command = command, time = time )
    async def send(self):
        while not builtins.client.is_closed():
            await builtins.commands[self.command]((self.channelid, self.guildid),*self.args, deletemsg=False)
            await asyncio.sleep(self.time) # task runs every 30 minutes

async def scheduleCreate(message, command, *args):
    args = list(args)
    if not args[-1][0].isdigit() and not args[-1][-1].lower() in ['m','h','d','w']:
        args.append('30m')
    print(args)
    await builtins.commands[command](message,*args[:-1])
    print(args)
    Schedule = schedule()
    await Schedule.setup(command, message = message, time = args[-1], args = args[:-1] )
    builtins.db.begin()
    builtins.ACtb.insert(Schedule.databaseformat)
    builtins.db.commit()
    builtins.client.loop.create_task(Schedule.send())
    pass

async def on_ready():
    for element in builtins.ACtb.find(type="s"):
        element = dict(element)
        Schedule = schedule()
        print(element)
        await Schedule.setup(element["command"], guildid= element["guildid"], channelid= element["channelid"], time = element["time"] , args = json.loads(element["args"].replace("'",'"')) )
        builtins.client.loop.create_task(Schedule.send())

async def __init__():
    builtins.commands.update({"schedule":scheduleCreate})
    builtins.events["on_ready"].append( on_ready )
