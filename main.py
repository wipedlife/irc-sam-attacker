#!/bin/python3.7
# -*- coding: cp1251 -*-
import sys,time # todo
#from irc import overlay
from irc import attacker
import configparser, asyncio
def main():
 if len(sys.argv) < 3:
  print (sys.argv[0]+" addr victim")
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
 a=attacker.attack(sys.argv[1], sys.argv[2])
 
 for bot in a.bots:
  bot.join()
 while True:
  pass
main()
