import builtins

#-- Module Start --#
async def UpdateDB():
    builtins.db.begin()
    for guild in builtins.client.guilds:
        builtins.Gtb.upsert(dict(id=guild.id, TopRole = guild.roles[-1].id, BothasTopRole = 1 if guild.me.top_role.id == guild.roles[-1].id else 0 ), ['id'])
        for role in guild.roles:
            builtins.Rtb.upsert(dict(id=role.id, name=role.name, guildid=guild.id, position=role.position), ['id'])
            for member in role.members:
                builtins.URtb.upsert(dict(roleid=role.id,userid=member.id, status=True, reason=None),["roleid","userid"])
        for member in guild.members:
            if not member.bot:
                userObject = builtins.client.get_user(member.id)
                if not userObject.dm_channel:
                    await userObject.create_dm()
                builtins.Utb.upsert(dict(id=member.id, name = userObject.display_name ,channel = userObject.dm_channel.id), ["id"])
                builtins.UGtb.upsert(dict(guildid=guild.id, userid=member.id),["guildid","userid"])
    builtins.db.commit()

async def __init__():
    builtins.events["on_ready"].append(UpdateDB)
