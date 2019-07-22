#!/bin/python3
# sudo apt install firefox-geckodriver
# proxychains ./update_openproxy.py

#https://splinter.readthedocs.io/en/latest/
import clipboard
from splinter import Browser
openproxy_url="https://www.proxy-list.download/SOCKS5"
#brow=Browser()
#brow.visit(openproxy_url)
proxy_file="openproxy_list.txt"

with Browser() as brow :
    brow.visit(openproxy_url)
    list=brow.find_by_id("txta1").click()

    proxy_list=clipboard.paste()
    with open(proxy_file,"w") as fb:
        fb.write(proxy_list)
