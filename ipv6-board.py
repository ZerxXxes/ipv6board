#!/usr/bin/env python3

from scapy.all import *
from queue import Queue
from threading import Thread
import dothat.backlight as backlight
import dothat.lcd as lcd
import time
import sys

# The /64 IPv6 prefix
prefix = "2001:6b0:1001:105"

# Read from the queue
def reader_proc(queue):
    # Create rows
    rows = [" "," "," "]
    backlight.hue(0.01)
    while True:
        # Move rows up
        rows[2] = rows[1]
        rows[1] = rows[0]
        newtext = queue.get()
        # Ignore repeded messages
        while newtext == rows[0]:
            newtext = queue.get()
        rows[0] = newtext
        print("1: %s" % rows[2])
        print("2: %s" % rows[1])
        print("3: %s" % rows[0])
        lcd.set_cursor_position(4,2)
        lcd.write(rows[0] + "     ")
        lcd.set_cursor_position(4,1)
        lcd.write(rows[1] + "     ")
        lcd.set_cursor_position(4,0)
        lcd.write(rows[2] + "     ")

        time.sleep(1)

# Listen to interface and write to the queue
def writer(queue):
    print("writer here")
    while True:
        sniff(prn=custom_action(queue),filter="icmp6 && ip6[40] == 128", count=1000)
        print("read 1000 packets")

# Process incoming ICMPv6-packets
def custom_action(queue):
    def parse_packet(pkt):
        if ICMPv6EchoRequest in pkt:
            # Flash leds to indicate ICMPv6 Echo packet received
            backlight.set_graph(1.0)
            backlight.set_graph(0.0)

            address = pkt[IPv6].dst
            # Strip prefix and leading 0s and colons
            address = address[len(prefix):]
            address = address.lstrip(":0")
            address = address.replace(":","")
            try:
                text = bytearray.fromhex(address).decode()
                queue.put(text)
            except Exception as e:
                print (e)
    return parse_packet

if __name__=='__main__':
    pqueue = Queue()
    print("start reader")
    reader_p = Thread(target=reader_proc, args=((pqueue),))
    reader_p.daemon = True
    reader_p.start()

    print("start writer")
    writer_p = Thread(target=writer, args=((pqueue),))
    writer_p.daemon = True
    writer_p.start()

    # If the queue starts to fill up, print its size
    while True:
        if pqueue.qsize() > 1:
            print("Queue size is: %s" % pqueue.qsize())
        time.sleep(5)
