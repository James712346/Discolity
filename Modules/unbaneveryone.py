import builtins

#-- Module Start --#
async def undogayban(guild, user):
    await guild.unban(user)

async def __init__():
    builtins.events['on_member_ban'].append(undogayban)
