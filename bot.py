import discord, builtins, os, importlib, traceback, configparser, dataset


ModuleFolder = "Modules"
ModulePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), ModuleFolder)
builtins.db = dataset.connect('sqlite:///data.sqlite')
builtins.db.begin()
builtins.Utb = builtins.db["user"]
builtins.Gtb = builtins.db["guilds"]
builtins.Rtb = builtins.db["roles"]
builtins.UGtb = builtins.db["UsersGuilds"]
builtins.URtb = builtins.db["UsersRoles"]
builtins.ACtb = builtins.db["ActiveCases"]
builtins.db.commit()

builtins.Module = [[f.replace(".py", ""), 0] for f in os.listdir(ModulePath) if not "__" in f]
builtins.client = discord.Client(activity=discord.CustomActivity("All for Gender Equality 👍"))
builtins.events = {
                    "on_ready":[], "on_member_join":[], "on_message":[],
                    "on_voice_state_update":[], "on_reaction_add":[],
                    "on_member_update":[], "on_guild_join": [],
                    "on_guild_update": [], "on_guild_role_delete":[],
                    "on_member_ban":[], "on_member_unban":[],
                    "on_relationship_update":[]
                  }

builtins.config = configparser.ConfigParser()

if not "config.ini" in os.listdir():
  modules = {}
  [ modules.update( {module:True} ) for module in [m[0] for m in builtins.Module] ]
  builtins.config["MAIN"] = { "Token":"","DEFUALTcommandSymbol":"!" }
  builtins.config["default_modules"] = modules
  with open('config.ini', 'w') as configfile:
      builtins.config.write(configfile)
else:
  builtins.config.read('config.ini')
  if len(builtins.config["default_modules"].keys()) < len(builtins.Module):
      builtins.config["default_modules"] = {}
      modules = {}
      [ modules.update( {module:True} ) for module in [m[0] for m in builtins.Module] ]
      builtins.config["default_modules"] = modules
      with open('config.ini', 'w') as configfile:
          builtins.config.write(configfile)


async def LoadModules(mod):
    try:
        Module = [ m for m in builtins.Module if mod in m ]
        if Module:
            Module = Module[0]
            if type(Module[1]) != int:
                importlib.reload(Module[1])
            else:
                Module[1] = importlib.import_module(ModuleFolder + "." + Module[0])
            await Module[1].__init__()
            return 0
        print("Error: No Module")
        return 1
    except Exception as e:
        Module[1] = 1
        print("".join(traceback.format_exception_only(e.__class__, e)))
        return 2

builtins.Tools = {"LoadModules":LoadModules}
builtins.commands = {}

@builtins.client.event
async def on_ready():
    for Modules in builtins.config["default_modules"]:
        if builtins.config["default_modules"][Modules] == 'True':
            await LoadModules(Modules)

    for event in builtins.events["on_ready"]:
        await event()

@builtins.client.event
async def on_member_join(member):
    for event in builtins.events["on_member_join"]:
        await event(member)

@builtins.client.event
async def on_message(message):
    for event in builtins.events["on_message"]:
        await event(message)

@builtins.client.event
async def on_voice_state_update(member, VCbefore, VCafter):
    for event in builtins.events["on_voice_state_update"]:
        await event(message, VCafter, VCbefore)

@builtins.client.event
async def on_reaction_add(reaction, member):
    for event in builtins.events["on_reaction_add"]:
        await event(reaction, member)

@builtins.client.event
async def on_member_update(Mbefore, Mafter):
    for event in builtins.events["on_member_update"]:
        await event(Mbefore, Mafter)

@builtins.client.event
async def on_guild_join(guild):
    for event in builtins.events["on_guild_join"]:
        await event(guild)

@builtins.client.event
async def on_guild_update(gbefore, gafter):
    for event in builtins.events["on_guild_update"]:
        await event(gbefore, gafter)

@builtins.client.event
async def on_guild_role_delete(role):
    for event in builtins.events["on_guild_role_delete"]:
        await event(role)

@builtins.client.event
async def on_member_ban(guild, user):
    for event in builtins.events["on_member_ban"]:
        await event(guild, user)

@builtins.client.event
async def on_member_unban(guild, user):
    for event in builtins.events["on_member_unban"]:
        await event(guild, user)

@builtins.client.event
async def on_relationship_update(brelation, arelation):
    for event in builtins.events["on_relationship_update"]:
        await event(brelation, arelation)

if __name__ == "__main__":
    builtins.client.run(builtins.config["MAIN"]["Token"])
