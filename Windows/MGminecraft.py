import sys
import os
import zipfile
import json
import time


def loadcfg(): #Frist Start?
    if os.path.isfile("hmcl.json"):
        pass
    else:
        print("[ERROR]Do not find HMCL cconfig")
        print("Maybe you need run HMCL frist")
        print("Exit now..")
        sys.exit()
    if os.path.isfile("MGconfig.json"):
        print("Loading MG config")
        tempfile = open("MGconfig.json","r")
        cfg = json.load(tempfile)
        tempfile.close()
        del tempfile
    else:
        print("Cannot find MG config")
        cfg = setup()
    return cfg

def setup():
    print("[Frist setup]")
    cfg = {}
    
    print("Enther Save Mode:")
    sel = input("1.root\n2.version\n")
    waitqueue = {"1":"root","2":"version"}
    if sel in waitqueue:
        cfg["mode"] = waitqueue[sel]
    del sel
    
    print("HMCLConfig: ")
    sel = input("(Default)\n")
    if sel:
        if not sel == "Default":
            cfg["HMCLConfig"] = sel    
    else:
        cfg["HMCLConfig"] = "Default"

    configfile = open("MGconfig.json","w")
    configfile.write(json.dumps(cfg,sort_keys=True, indent=4, separators=(',', ': ')))
    configfile.close()
    return cfg


class MGcore(object):
    def __init__(self,config):
        self.config = config
        self.HMCLloader()

    def HMCLloader(self):
        print("[MGcore]Reading HMCL config")
        tempfile = open("hmcl.json","r") #Work with HMCL
        HMCL = json.load(tempfile)
        tempfile.close()
        del tempfile
        self.config["version"] = HMCL["configurations"][self.config["HMCLConfig"]]["selectedMinecraftVersion"]
        if self.config["mode"] == "root":
            self.config["location"] = os.path.join(HMCL["configurations"][self.config["HMCLConfig"]]["gameDir"].replace("\\","/"), "saves")
            #Join path:gamedir(format with "/") + saves[ROOT MODE]
        elif self.config["mode"] == "version":
            self.config["location"] = os.path.join(HMCL["configurations"][self.config["HMCLConfig"]]["gameDir"].replace("\\","/"), "versions", self.config["version"], "saves")
            #Join path:gamedir(format with "/") + version + version name + saves[VERSION MODE]
    
    def save_finder(self):
        savelist = []
        for root, dirs, files in os.walk(self.config["location"]):
            if "level.dat" in files:
                savelist.append(os.path.basename(root))
            else:
                pass
        return savelist

    def save_zipper(self,save):
        zipname = save + "-" + time.strftime("%Y%m%d%H%M%S", time.localtime())
        szip = zipfile.ZipFile(zipname, "w")
        for root, dirs, filesname in os.walk(os.path.join(self.config["location"], save)):
            for files in filesname:
                folder = os.path.join(root,files)
                print("Writing file: " + folder)
                szip.write(folder,compress_type=zipfile.ZIP_LZMA)
        szip.close()
        if os.path.isfile("MGsave.save"):
            MGsave = zipfile.ZipFile("MGsave.save", "a")
            MGsave.write(zipname, compress_type=zipfile.ZIP_DEFLATED)
            MGsave.close()
        else: #New file
            MGsave = zipfile.ZipFile("MGsave.save", "w")
            MGsave.write(zipname, compress_type=zipfile.ZIP_DEFLATED)
            MGsave.close()
        os.remove(zipname)
        print("Read a save successful")

class MGfunction(object):
    def __init__(self,core):
        self.MGcore = core
        self.allfunction = ["help","reload","start","save","exit"]
        print("Type 'help' to help")

    def input(self,comm):
        comm = comm.split()
        if comm == []:
            return 1,self.MGcore
        if comm[0] in self.allfunction:
            arg = comm[1:]
            call = "self." + comm[0] + "(" + str(arg) + ")"
            exitcode = eval(call) #Call need function
        else:
            print("[ERROR]Unknown command")
            exitcode = 1
        return exitcode, self.MGcore

    def help(self,arg):
        commlist = "Allow command list:\n"
        for x in self.allfunction:
            commlist = commlist + x + "\n"
        print(commlist)
        return 1, self.MGcore

    def reload(self,arg):
        if arg == []:
            print("Use 'reload /t [hmcl/all] to reload config file")
        elif arg[0] == "/t":
            arg.pop(0)
            if arg[0] == "hmcl":
                print("Reloading HMCL config")
                self.MGcore.HMCLloader()
            elif arg[0] == "all":
                print("Reloading all config")
                self._reloadcfg()
            else:
                print("[ERROR]Unkonwn type")
        return 1,self.MGcore

    def _reloadcfg(self): #Reload MG config and HMCL config
        self.MGcore.config = loadcfg()
        self.MGcore.HMCLloader()

    def start(self,arg):
        filelist = os.listdir() #Find HMCL exe file
        pullup = False
        for x in filelist:
            name = x.split("-")
            if "HMCL" in name and os.path.splitext(x)[-1:] == "exe":
                print("Starting HMCL Luncher")
                os.system(x)
                pullup = True
                break
        if pullup:
            print("HMCL Luncher exit.")
        else:
            print("[ERROR]HMCL has not find")
        return 1, self.MGcore

    def save(self,arg):
        savelist = self.MGcore.save_finder()
        if arg == []:
            print("Use 'save [SaveName]' to reading Minecraft save")
            findsave = "Find saves:"
            for x in savelist:
                findsave = findsave + x + "\n"
            print(findsave)
        elif arg[0] in savelist: #Need to cut [] head(input contant: "[save]" is string)
            self.MGcore.save_zipper(arg[0])
        else:
            print("[ERROR]Cannot find this save,check it out")
        return 1, self.MGcore

    def exit(self,arg):
        print("Exit user CUI")
        sys.exit()

def luncher():
    print("Minecrfat MG by Tiya Anlite")
    print("Checking up and Loading MG config......")
    config = loadcfg()
    print("Creating and Loading HMCL config......")
    MG = MGcore(config)
    print("Pull up user space")
    MGF = MGfunction(MG)
    while True:
        comm = input()
        exitcode, MG = MGF.input(comm)

#Main
luncher()