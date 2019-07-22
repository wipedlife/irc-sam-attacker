import configparser
class config_bot:
    config = configparser.ConfigParser()
    ignore_chns=[]
    def del_bytes(self,line,minord=32):
        return ''.join([z for z in line if ord(z) >= minord])
    def __init__(self,fn="config.ini"):
        print("Config is inited")
        self.config.read(fn)
        self.ignore_chns=self.config["BOT"]['ignore_chns'].split(',')