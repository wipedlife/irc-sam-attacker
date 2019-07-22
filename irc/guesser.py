# -*- coding: cp1251 -*-
from .overlay import IRCOverlay
import configparser, sys, threading, random, string,time, asyncio, re
from string import digits
from .config_bot import config_bot as conf_bot

class guesser(conf_bot):
    def rand_string(self, size=8):
     return ''.join(random.choice(string.ascii_lowercase) for i in range(size))
    base_a={}
    irc=IRCOverlay(None,None,None,None)
    bot_nick=""
    tmp_n_ask=""
    score=0
    def init_base(self):
       try:
        fb=open(self.config["GUESSER"]['file'],"r+",encoding=self.config["CONNECTION"]['encoding'])
        data = fb.read().split('\n')
        for d in data:
               d=self.del_bytes(d)
               d=d.lower()
               splited=d.split('|')
               if len(splited) ==2:
                #splited[0]=''.join([char for char in splited[0] if char.isalpha() or char.isspace()])
                #print("Add to base %s|%s" %(splited[0].lower(),splited[1].lower()))
                self.base_a[splited[0]]=splited[1]
       except UnicodeDecodeError as err:
           print("Try other encoding... %s (raise..)\n" % (err) )
           raise err
 #      print("Read base: ")
#       for b in self.base_a:
#           print("%s|%s" % (b, self.base_a[b]))

  #     print("End of base.")

    def loop(self):
     try:
       data = self.irc.oread()
       for line in data.split('\n'):
           print("Line is : %s " % (line) )
           spl = line.split(' ')
           if ('PONG' in line or 'PING' in line) and (len(spl) == 4 and spl[2] in spl[0] or len(spl) == 2):
               self.irc.pong(spl[1])
           if len(spl) > 4:
               if spl[1] == 'PRIVMSG':                       
                   useri = self.irc.getuser(spl[0])

                   msg = ' '.join(spl[3:][2:]).lower()
                   msg=' '.join(msg.split(' ')[0:])


                   msgs=msg.split('(')
                   if len(msgs) == 2:
                       msg=msgs[0]
                   msg = re.sub(r"[\x02\x1F\x0F\x16]|\x03(\d\d?(,\d\d?)?)?", "", msg).rstrip()
                   chn=spl[2]
                   if useri["nick"] == self.bot_nick:
                       if random.randint(0, 300) == 190:
                           fatality_phrase="Ну что гугляры, поиграем в игру?"
                           self.irc.privmsg(chn,fatality_phrase)

                       if self.tmp_n_ask !="" and ("Верный ответ" in line or "правильный ответ" in msg or "Точный ответ" in msg or "Правильный ответ -> " in msg):
                         shitcode=""
                         if "правильный ответ" in msg:
                             shitcode=msg.split(' - ')[1].strip()
                         else:
                          shitcode=((line.split("-> ")[1]).split('" <-')[0])[1:].strip()
                         exist=False
                         for key in self.base_a:
                             if key in self.tmp_n_ask:
                                 exist=True
                                 print("Answer exist")
                         if not exist:
                          if '"' in shitcode:
                               shitcode = shitcode.split('"')[1].split(' ')[0]
                          print("New ask %s = %s" % (self.tmp_n_ask, shitcode))
                          shitcode=shitcode.lower()
                          shitcode=''.join([char for char in shitcode if char.isalpha()])
                          self.tmp_n_ask=self.tmp_n_ask.lower()
                          self.base_a[self.tmp_n_ask]=shitcode
                          fb=open(self.config["GUESSER"]['file'],"a+",encoding=self.config["CONNECTION"]['encoding'])
                          print("write to file %s|%s\n" % (self.tmp_n_ask,shitcode))
                          fb.write("%s|%s\n" % (self.tmp_n_ask,shitcode))
                          fb.close()
                          self.tmp_n_ask=""
                          return True
                       if "букв" in line and "(" in line and ")" in line:

                        self.tmp_n_ask=msg.strip().split('(')[0]
                        print("I will add new answer for ask %s" % (self.tmp_n_ask))
                       msg=msg.split('(')[0]
                       print("bot %s with hostname %s write message on %s -> %s" % (useri["nick"], useri["host"], chn, msg))
                       if len(msg) > 0:
                        print("Search in base %s" % (msg) )
                        for key in self.base_a:
                           if key in msg :
                            print("Yeeh write! %s in %s" %(key,msg))
                            self.irc.privmsg(chn, self.base_a[key])
                           # answ=self.irc.oread()
                          #  if self.bot_nick in answ:
                            # self.score=answ.split('.')[2].split()[3]
                            pass

                            return True
     except Exception as err:
         print( str(err) )
         pass
                       
                   
    def __init__(self, serv,channel,bot_nick,port=6667):
        super().__init__()
        self.init_base()
        self.irc=IRCOverlay(serv,self.rand_string(),self.rand_string(),self.rand_string(),p=port)
        self.bot_nick=bot_nick
        self.irc.cjoin(channel)
        self.irc.privmsg(channel,"!start")
        while True:
         self.loop()
         
        pass

class Guesser_Flooder_Thread(threading.Thread):
    bot=None
    dest=""
    chn=""
    victim=""
    port=6667
    def __init__(self,dest,chn,victim,port):
     super(Guesser_Flooder_Thread, self).__init__()
     self.dest=dest
     self.chn=chn
     self.victim=victim
     self.port=port
     pass
    def run(self):
        print("Thread of flooder init")
        bot = guesser(self.dest, self.chn, self.victim,port=self.port)
        pass

class Guesser_Flooder:
    threads=[]
    def __init__(self,dest,chn,victim,count=60,pause_bot=5,port=6667):
     while True:
       for i in range(0,count):
         print("Add thread of bot")
         self.threads.append(Guesser_Flooder_Thread(dest,chn,victim,port=port))

       for bot in self.threads:
         bot.start()
         time.sleep(pause_bot)
       for bot in self.threads:
           bot.join()
