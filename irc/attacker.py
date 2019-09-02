# -*- coding: cp1251 -*-
from .overlay import IRCOverlay
import configparser, sys, threading, random, string,time, asyncio
from . import config_bot as conf_bot

class BotAttack(threading.Thread):
 irc=IRCOverlay(None,None,None,None)
 victim=""
 nick=""
 username=""
 realname=""
 dest=""
 sleepTime=0
 p=0
 victim_channels=[]
 my_channels=[]
 victim_info=[]
 cfg=conf_bot.config_bot()
 async def update_config(self,nick):
  vic = self.irc.read_cfg("victims.ini")
  vic[self.victim]['nick']=nick
  with open("victims.ini", "w+") as victim_file:
   vic.write(victim_file)
 def victim_ini_init(self):
  vic = self.irc.read_cfg("victims.ini")
  if not self.victim in vic:
   if self.victim_info == []:
    victim_info=self.irc.whois(self.victim)
    #todo: search by hostname
    tmp={}
    print("init vimctim_info")
    for info in victim_info:
     print("Info %s" % (info))
     print("Value: %s " % (victim_info[info]))

     tmp[info]=victim_info[info]
     with open("victims.ini", "w+") as victims_file:
      vic[self.victim]=tmp
      vic.write(victims_file)
      pass

 def __init__(self,serv,victim,nick,username,realname,p=6667):
  self.victim=victim
  self.nick=nick
  self.username=username
  self.realname=realname
  self.dest=serv
  self.p=p
  super(BotAttack, self).__init__()

 async def getVictimChannels(self):
  self.victim_channels = self.irc.getChannels(self.victim)
  if self.victim_channels == False:
   return False
  for chn in self.victim_channels:
    if chn in self.irc.config['BOT']['ignore_chns'].split(','):
     continue
    if not chn in self.my_channels:
     if chn[0] != '#':
      chn=chn[1:]
      if chn !='#':
       continue
     print("join to %s" % (chn))
     self.irc.cjoin(chn)
     self.my_channels.append(chn)
 async def update_own_channels(self):
  for chn in self.my_channels:
    if not chn in self.victim_channels:
     self.irc.leave(chn)
     self.my_channels.remove(chn)
     pass
 async def trollVictim(self):
  for chn in self.my_channels:
   print("Write to %s msg" % (chn))
   #todo: fix (Line: :XXX XXX XXX :No recipient given (PRIVMSG))
   with open('phrases.txt','r+',encoding="cp1251") as phrasesf:
    phrases=(phrasesf.read()).split("\n")
   # print(phrases)
    if len(phrases) == 0:
     self.irc.privmsg(chn,"%s Trololo" % (self.victim)) #Trololo
     self.irc.privmsg(self.victim,"%s Trololo " %(self.victim)) # Trololo
    else:
     phras=str( phrases[  random.randrange(len(phrases)) ] )
     self.irc.privmsg(chn, "%s %s" % (self.victim, phras ))  # Trololo
     self.irc.privmsg(self.victim, "%s %s " % (self.victim,phras ))  # Trololo

 async def chase_victim(self):

  pass
 async def loop(self):
  while True:
   if await self.getVictimChannels() == False:
    time.sleep(30*60)
   await self.chase_victim()
   await self.trollVictim()
   c,newnick=await self.irc.hand.handl(self.victim)
   if c:
    print("New nick is %s " % (newnick))
    await self.update_config(self.victim)
    self.victim = newnick
   await self.update_own_channels()
   await asyncio.sleep(self.sleepTime)
   pass

 def run(self):
  self.irc=IRCOverlay(self.dest,
  self.nick,
  self.username,
  self.realname, p=self.p)
  print("Bot %s inited" % (self.nick) )
  self.victim_ini_init()
  asyncio.run(asyncio.coroutine(self.loop)())


class attack():
 victim=""
 botsM=0
 bots=[]

 def rand_string(self, size=8):
  return ''.join(random.choice(string.ascii_lowercase) for i in range(size))

 def __init__(self, serv,victim, count=30, nicks_from_file=False,nicklength=8,pause_bot=60,sleepTime=20, p=6667):
  self.victim=victim
  self.sleepTime = sleepTime
  nicks=[]
  if nicks_from_file:
     with open('Nicks','r') as nicksf:
      nicks=nicksf.read().split('\n')
  else:
     for bot in range(1,count):
      nicks.append(self.rand_string())
  for nick in nicks:
       self.bots.append( BotAttack(serv, victim, nick, self.rand_string(), self.rand_string(),p=p)  )

#       time.sleep(5)
       for bot in self.bots:
        try:
         print("Start bot...")
         bot.start()
         time.sleep(pause_bot)
        except RuntimeError:
         pass

