import builtins

async def who(guild, user):
    for i in guild.audit_logs(limit=10):
        print(i)
    pass

def __init__():
    builtins.events["on_member_ban"].append(who)
