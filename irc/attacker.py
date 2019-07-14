# -*- coding: cp1251 -*-
from .overlay import IRCOverlay
import configparser, sys, threading, random, string,time, asyncio

class BotAttack(threading.Thread):
 irc=IRCOverlay(None,None,None,None)
 victim=""
 nick=""
 username=""
 realname=""
 dest=""
 sleepTime=0
 victim_channels=[]
 my_channels=[]
 def __init__(self,serv,victim,nick,username,realname):
  self.victim=victim
  self.nick=nick
  self.username=username
  self.realname=realname
  self.dest=serv
  super(BotAttack, self).__init__()

 async def getVictimChannels(self):
  self.victim_channels = self.irc.getChannels(self.victim)
  for chn in self.victim_channels:
    if not chn in self.my_channels:
     self.irc.cjoin(chn)
     self.my_channels.append(chn)


 async def trollVictim(self):
  for chn in self.my_channels:
   if "@" in chn:
    chn=chn[1:]
   self.irc.privmsg(chn,"%s Trololo" % (self.victim)) #Trololo
   self.irc.privmsg(self.victim,"%s Trololo " %(self.victim)) # Trololo

  pass
 async def loop(self):
  while True:
   await self.getVictimChannels()
   await self.trollVictim()
   await self.irc.hand.handl()
   await asyncio.sleep(self.sleepTime)
   pass

 def run(self):
  self.irc=IRCOverlay(self.dest,
  self.nick,
  self.username,
  self.realname)
  print("Bot %s inited" % (self.nick) )
  asyncio.run(asyncio.coroutine(self.loop)())


class attack():
 victim=""
 botsM=0
 bots=[]

 def __init__(self, serv,victim, count=2, nicks_from_file=False,nicklength=8,pause_bot=30,sleepTime=30):
  self.victim=victim
  self.sleepTime = sleepTime
  nicks=[]
  if nicks_from_file:
     with open('Nicks','r') as nicksf:
      nicks=nicksf.read().split('\n')
  else:
     for bot in range(1,count):
      nicks.append(''.join(random.choice(string.ascii_lowercase) for i in range(nicklength)))
  for nick in nicks:
       self.bots.append( BotAttack(serv, victim, nick, nick, nick)  )
       for bot in self.bots:
        try:
         print("Start bot...")
         bot.start()
         time.sleep(pause_bot)
        except RuntimeError:
         pass

