#!/bin/python3.7
import asyncio,sys # todo 
from irc import overlay
import configparser
def main():
# if len(sys.argv) < 5:
#  print (sys.argv[0]+" Nick realname username Addr")
#  sys.exit()
#  print ( "Init" )
 config=configparser.ConfigParser()
 config.read("config.ini")
 config=config["BOT"]
 #def __init__(self,dest,nick,username,realname):
 irc=overlay.IRCOverlay(config["serv_addr"],
                        config["nick"],
                        config["username"],
                        config["realname"])
 irc.cjoin("#testbot")
 irc.hand.commands()

main()

