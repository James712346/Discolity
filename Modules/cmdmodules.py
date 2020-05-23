import builtins

#-- Module Start --#

async def GetModules(message):
    statusList = []
    for module in builtins.Module:
        if type(module[1]) != int:
            statusList.append([module[0], "```diff\n+ loaded\n```"])
        elif module[1]:
            statusList.append([module[0], "```diff\n- broken!\n```"])
        else:
            statusList.append([module[0], "```diff\n/ unloaded\n```"])
    await builtins.Tools["responsemsg"](message, "Module Status's",
                                    "All of the commands (but 3) are run through Modules that can be unloaded or loaded at will", *statusList)

async def LoadModules(message, Module):
    Response = await builtins.Tools["LoadModules"](Module)
    if Response:
        await builtins.Tools["errormsg"](message, "No Module Called that", "The Module doesn't exist or couldn't be found!", ["Inputted Module", Module])
    elif not Response:
        await builtins.Tools["responsemsg"](message, "Module Loaded", Module.title() + "has been success loaded onto the bot")
    else:
        await builtins.Tools["errormsg"](message, "Module Error", "The Module Errored, this module is broken and will need to be fixed!\n ```bash\n" + "".join(traceback.format_exception_only(e.__class__, e)) + "\n```")

async def __init__():
    builtins.commands.update( { "status":GetModules, "load":LoadModules } )
    pass
