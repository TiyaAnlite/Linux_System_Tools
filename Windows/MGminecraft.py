import os
import zipfile
import json
import time


def loadcfg(): #Frist Start?
    if os.path.isfile("MGcfg.json"):
        tempfile = open("MGconfig.json","r")
        cfg = json.load(tempfile.read())
        tempfile.close()
        del tempfile
        luncher(cfg)
    else:
        cfg = setup()
        luncher(cfg)
    return cfg

def setup():
    print("[Frist setup]")
    cfg = {}
    
    print("Enther Save Mode:")
    sel = input("1.root\n2.version\n")
    waitqueue = {1:"root",2:"version"}
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
        tempfile = open("hmcl.json","r") #Work with HMCL
        HMCL = json.load(tempfile.read())
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

    def save_zipper(self,save,time):
        zipname = time.strftime("%Y%m%d%H%M%S", time.localtime())
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

def luncher(config):
    print("Minecrfat MG by Tiya Anlite")
    print("Checking up and Loading MG config......")
    config = loadcfg()
    print("Creating and Loading HMCL config......")
    MG = MGcore(config)