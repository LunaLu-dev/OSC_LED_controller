"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import urllib
import os
import subprocess
import urllib3
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

def as_bool(value) -> bool:
    # OSC can deliver bools, ints, floats, or strings depending on sender
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"1", "true", "t", "yes", "y", "on"}:
            return True
        if v in {"0", "false", "f", "no", "n", "off", ""}:
            return False
    raise ValueError(f"Can't interpret as bool: {value!r} ({type(value).__name__})")

def owo_mode(unused_addr, *args):
    raw = args[0] if args else False
    ene = as_bool(raw)
    print(f"OWO MODE: {ene}")
    if ene == True:
        urllib3.request('POST', 'http://192.168.1.221:9000/hooks/busy-red')
        print("OwO Protocol Starting Intiface")
        subprocess.Popen("C:/Users/lunan/AppData/Roaming/IntifaceCentral/intiface_central.exe")
        print("OwO Protocol Starting OSC_GO_BRR")
        subprocess.Popen("C:/Users/lunan/AppData/Local/Programs/OscGoesBrrr/OscGoesBrrr.exe")

def led_handler(unused_addr, *args):
    led_value = args[0] if args else 0
    if led_value == 0:
        return
    elif led_value == 1:
        print("LED GREEN")
        urllib3.request( 'POST', 'http://192.168.1.221:9000/hooks/busy-green')
    elif led_value == 2:
        print("LED YELLOW")
        urllib3.request('POST', 'http://192.168.1.221:9000/hooks/busy-yellow')
    elif led_value == 3:
        print("LED RED")
        urllib3.request('POST', 'http://192.168.1.221:9000/hooks/busy-red')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=9001, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = Dispatcher()
  dispatcher.map("/avatar/parameters/led", led_handler)
  dispatcher.map("/avatar/parameters/owo-mode", owo_mode)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()