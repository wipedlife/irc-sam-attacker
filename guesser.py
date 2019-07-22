#!/bin/python3.7
# -*- coding: cp1251 -*-
import sys,time # todo
#from irc import overlay
from irc import guesser
import configparser, asyncio
def main():
 if len(sys.argv) < 3:
  print (sys.argv[0]+" serv channel bot_nick")
  sys.exit()
#  print ( "Init" )
# config=configparser.ConfigParser()
# config.read("config.ini")
# config=config["BOT"]
 #def __init__(self,dest,nick,username,realname):
 #irc=overlay.IRCOverlay(config["serv_addr"],
#                        config["nick"],
#                        config["username"],
#                        config["realname"])
 #irc.cjoin("#testbot")
 #irc.hand.commands()
 a=guesser.guesser(sys.argv[1], sys.argv[2], sys.argv[3])
 
 for bot in a.bots:
  bot.join()
 while True:
  pass
main()
