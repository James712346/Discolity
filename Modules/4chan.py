import builtins, basc_py4chan, Log, random, os, discord
Save_Channel = "saves"
icons = {
    '3': 'https://i.ibb.co/g7v4mx7/3-logo.png',
    'a': 'https://i.ibb.co/09CmRpn/A-logo.png',
    'aco': 'https://i.ibb.co/dWky78d/Aco-logo.png',
    'adv': 'https://i.ibb.co/bJvkSjc/Adv-logo.png',
    'an': 'https://i.ibb.co/2jrg5GV/An-logo.png',
    'asp': 'https://i.ibb.co/HBc2Ztz/Asp-logo.png',
    'b': 'https://i.ibb.co/qpS2qwT/B-logo.png',
    'bant': 'https://i.ibb.co/h9GVrb5/Bant-logo.png',
    'c': 'https://i.ibb.co/rZWnMF7/C-logo.png',
    'cgl': 'https://i.ibb.co/3MrTpft/Cgl-logo.png',
    'biz': 'https://i.ibb.co/3sns3z4/Biz-logo.png',
    'ck': 'https://i.ibb.co/RBN1VmY/Ck-logo.png',
    'cm': 'https://i.ibb.co/LCcCfPv/Cm-logo.png',
    'co': 'https://i.ibb.co/xDkQWGp/Co-logo.png',
    'd': 'https://i.ibb.co/Bc6k947/D-logo.png',
    'diy': 'https://i.ibb.co/8DG8cDc/Diy-logo.png',
    'e': 'https://i.ibb.co/G9x5Kgq/E-logo.png',
    'f': 'https://i.ibb.co/b705FFm/F-logo.png',
    'fa': 'https://i.ibb.co/y8Tt1QH/Fa-logo.png',
    'fit': 'https://i.ibb.co/mhwC8gm/Fit-logo.png',
    'g': 'https://i.ibb.co/ydY95sg/G-logo.png',
    'gif': 'https://i.ibb.co/4TpDH6V/Gif-logo.png',
    'h': 'https://i.ibb.co/sKvDqxb/H-logo.png',
    'gd': 'https://i.ibb.co/fDF0y5d/Gd-logo.png',
    'his': 'https://i.ibb.co/WGNwvkZ/His-logo.png',
    'hr': 'https://i.ibb.co/rHhZ6R2/Hr-logo.png',
    'i': 'https://i.ibb.co/gtLJxtF/I-logo.png',
    'hm': 'https://i.ibb.co/XXQ2ySv/Hm-logo.png',
    'int': 'https://i.ibb.co/HqZxXPc/Int-logo.png',
    'jp': 'https://i.ibb.co/vkfSKzh/Jp-logo.png',
    'k': 'https://i.ibb.co/s5Q4z2s/K-logo.png',
    'ic': 'https://i.ibb.co/qxsvkdN/Ic-logo.png',
    'lgbt': 'https://i.ibb.co/gFkSnTk/Lgbt-logo.png',
    'm': 'https://i.ibb.co/SXFsQFX/M-logo.png',
    'mlp': 'https://i.ibb.co/KN6MJGf/Mlp-logo.png',
    'mu': 'https://i.ibb.co/KVh88kj/Mu-logo.png',
    'lit': 'https://i.ibb.co/KrZrWrg/Lit-logo.png',
    'n': 'https://i.ibb.co/FnCNB7P/N-logo.png',
    'o': 'https://i.ibb.co/jJDpKch/O-logo.png',
    'out': 'https://i.ibb.co/DkBZmLD/Out-logo.png',
    'p': 'https://i.ibb.co/9VF5sgN/P-logo.png',
    'po': 'https://i.ibb.co/y4rWQQS/Po-logo.png',
    'pol': 'https://i.ibb.co/9nq5QFG/Pol-logo.png',
    's': 'https://i.ibb.co/GkWwkj7/S-logo.png',
    'r9k': 'https://i.ibb.co/jD4GJxC/R9k-logo.png',
    's4s': 'https://i.ibb.co/dQs2rYv/S4s-logo.png',
    'sci': 'https://i.ibb.co/kMfvYFZ/Sci-logo.png',
    'sp': 'https://i.ibb.co/1fZNRGK/Sp-logo.png',
    't': 'https://i.ibb.co/0DhWfpT/T-logo.png',
    'soc': 'https://i.ibb.co/q576mpq/Soc-logo.png',
    'tg': 'https://i.ibb.co/zXQFYz1/Tg-logo.png',
    'trv': 'https://i.ibb.co/JnZC18H/Trv-logo.png',
    'toy': 'https://i.ibb.co/kSdF64w/Toy-logo.png',
    'tv': 'https://i.ibb.co/Bt0g24w/Tv-logo.png',
    'v': 'https://i.ibb.co/4FJ7g6Y/V-logo.png',
    'vg': 'https://i.ibb.co/YTVDDK3/Vg-logo.png',
    'u': 'https://i.ibb.co/vdQCjk7/U-logo.png',
    'vr': 'https://i.ibb.co/Tq5MVg4/Vr-logo.png',
    'vp': 'https://i.ibb.co/wwVCddq/Vp-logo.png',
    'w': 'https://i.ibb.co/ZLTdT3F/W-logo.png',
    'wg': 'https://i.ibb.co/LRQ1kfQ/Wg-logo.png',
    'x': 'https://i.ibb.co/1v55b5s/X-logo.png',
    'y': 'https://i.ibb.co/KDHKH66/Y-logo.png',
    'wsg': 'https://i.ibb.co/f0GTPHR/Wsg-logo.png'
    }

async def PostFind(message, board, thread="", post="", deletemsg=True):
    if "https://boards.4chan.org/" in board or "https://boards.4chan.org/" in board :
        tb = board.replace("https://boards.4chan.org/","").replace("http://boards.4chan.org/","").replace("/thread/","/").replace("#p","/").split("/")
        thread = tb[1]
        board =  tb[0]
        if len(tb) > 2:
            if tb[2].isdigit():
                post = tb[2]
    Board = basc_py4chan.get_boards(board)[0]
    if thread != "":
        Thread = basc_py4chan.Thread(Board,int(thread))
    else:
        Thread = basc_py4chan.Thread(Board,random.choice(Board.get_all_thread_ids()))
    Thread.update()
    if post:
        topic = [p for p in Thread.all_posts if p.post_id == int(post)][0]
    else:
        topic = Thread.topic
    url = ""
    icon = icons[Board.name] if Board.name in icons else ""
    title = topic.subject if topic.subject else topic.text_comment[:20].replace("\n","")+ "..." if len(topic.text_comment) > 20 else ""
    extra = {"Posts":len(Thread.all_posts), "Archive":Thread.archived, "Closed": Thread.closed}
    if topic.has_file:
        url = topic.file1.file_url
    await builtins.Tools["webhook"](message.channel, title, url, Board.title, icon, topic.url.replace("http","https"), extra, "found by "+ message.author.display_name +"\nfound at https://boards.4channel.org/" + Board.name+"/", topic.text_comment)
    if deletemsg:
        await message.delete()

async def __init__():
    builtins.commands.update( { "4chan" : PostFind } )
    Log.Verbose("4chan has started")
