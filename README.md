# irc-sam-attacker
## Usage
./main.py <addr> <victim> <port> -> flood to victim
./guesser.py <addr> <victim> <port> -> anti-quiz bot
./gen_nicks.sh count -> gen file of nicks (Nicks)
proxychains ./update_openproxy.py -> update open proxy list to openproxy_list.txt
### Config options
```
[CONNECTION]
type=tor/clear/openproxy/i2p 

i2p=connect by a SAM
clear=connect by a socket
openproxy=connect by a openproxy
tor=connect by Tor

tor_port=9050 -> port of tor 
encoding=UTF-8/cp1251/...

[BOT]
nick=Botyara -> nick of the bot for friend type
username=UserName -> username of the bot for friend type
realname=RealName -> too ...
serv_addr=irc.ilita.i2p -> ... deprecated ...
ignore_chns=#expert,#expert1 -> channels here will be ignored by flooder.
base_channel=#testbot -> default channel of the bot for friend type

[OWNER]
nick=L  -> ...
hostname=a@a.b32.i2p -> ...

[GUESSER]
file=3hauka-utf.txt -> file of dictionary for anti-quiz mode
```
