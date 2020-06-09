import os, time
os.system("")
last_log = time.time()

class TextFormat:
    END      = '\33[0m'
    BOLD     = '\33[1m'
    ITALIC   = '\33[3m'
    URL      = '\33[4m'
    BLINK    = '\33[5m'
    BLINK2   = '\33[6m'
    SELECTED = '\33[7m'
    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE  = '\33[36m'
    WHITE  = '\33[37m'
    BLACKBG  = '\33[40m'
    REDBG    = '\33[41m'
    GREENBG  = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG   = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG  = '\33[46m'
    WHITEBG  = '\33[47m'
    GREY    = '\33[90m'
    RED2    = '\33[91m'
    GREEN2  = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2   = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2  = '\33[96m'
    WHITE2  = '\33[97m'
    GREYBG    = '\33[100m'
    REDBG2    = '\33[101m'
    GREENBG2  = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2   = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2  = '\33[106m'
    WHITEBG2  = '\33[107m'
def fileadd(msg):
    with open('events.log',"a") as f:
        f.write(" ".join(msg)+"\n")

def Verbose(*inputed):
    Type, Time = "VERBOSE", "%.2f" % round(time.time(),2)
    inputed = [i.replace('\n','\n'+(" "*(len(Type)+len(Time)+4))+'| ') if type(i) == str else str(i) for i in inputed]
    msg = (Time, "|",TextFormat.GREY + "VERBOSE |", *inputed,TextFormat.END)
    print(*msg)
    fileadd(msg)

def Log(*inputed):
    Type, Time = "VERBOSE", "%.2f" % round(time.time(),2)
    inputed = [i.replace('\n','\n'+(" "*(len(Type)+len(Time)+4))+'| ') if type(i) == str else str(i) for i in inputed]
    msg = (Time, "|","LOGGING |", *inputed)
    print(*msg)
    fileadd(msg)

def Success(*inputed):
    Type, Time = "VERBOSE", "%.2f" % round(time.time(),2)
    inputed = [i.replace('\n','\n'+(" "*(len(Type)+len(Time)+4))+'| ') if type(i) == str else str(i) for i in inputed]
    msg = (Time, "|",TextFormat.GREEN + "SUCCESS |", *inputed ,TextFormat.END)
    print(*msg)
    fileadd(msg)

def Error(*inputed):
    Type, Time = "VERBOSE", "%.2f" % round(time.time(),2)
    inputed = [i.replace('\n','\n'+(" "*(len(Type)+len(Time)+4))+'| ') if type(i) == str else str(i) for i in inputed]
    msg = (Time, "|",TextFormat.WHITE + TextFormat.REDBG + TextFormat.BLINK +"!ERROR!"+TextFormat.END+TextFormat.RED,"|", *inputed, TextFormat.END)
    print(*msg)
    fileadd(msg)

def Warning(*inputed):
    Type, Time = "VERBOSE", "%.2f" % round(time.time(),2)
    inputed = [i.replace('\n','\n'+(" "*(len(Type)+len(Time)+4))+'| ') if type(i) == str else str(i) for i in inputed]
    msg = (Time, "|", TextFormat.WHITE + TextFormat.YELLOWBG + "WARNING"+TextFormat.END+TextFormat.YELLOW,"|",*inputed, TextFormat.END)
    print(*msg)
    fileadd(msg)

def on_modified(event):
    global last_log
    if event.src_path == ".\events.log":
        with open(event.src_path, "r") as f:
            toPrint = []
            Msglength = 0
            Fline = []
            for line in f.readlines()[::-1]:
                line = line.replace("\\33","\33")
                Time = line.split("|")[0]
                if Time.strip() != "":
                    if float(Time) < last_log:
                        break
                    toPrint.insert(0,line+"".join(Fline))
                    last_log = float(Time)
                    Fline = []
                else:
                    Fline.insert(0,line)
            print("".join(toPrint[Msglength:]).strip("\n"))

def PrintLogs(file):
    with open(file, "r") as f:
        print(f.read().strip("\n"))

if __name__ == "__main__":
    option = input("Live input or Read Logs or both (L/R/LR)").lower()
    if 'r' in option:
        PrintLogs("./events.log")
    if "l" in option:
        from watchdog.observers import Observer
        from watchdog.events import PatternMatchingEventHandler
        patten_requirements = PatternMatchingEventHandler(patterns='*.log',case_sensitive=True)
        patten_requirements.on_modified = on_modified
        file_watcher = Observer()
        file_watcher.schedule(patten_requirements, ".", recursive=True)
        file_watcher.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            file_watcher.stop()
            file_watcher.join()
    print("Goodbye")
else:
    os.remove("./events.log")
