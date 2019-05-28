import sys
import argparse
import threading
import time
import re

from pyOpenBCI import OpenBCICyton, OpenBCIWiFi
if sys.platform.startswith("linux"):
    from pyOpenBCI import OpenBCIGanglion


if __name__ ==  '__main__':
    parser = argparse.ArgumentParser(description='Interface with OpenBCI boards using Python.')
    parser.add_argument('--board', action='store', default=None, help="Choose a board ['Cyton', 'CytonDaisy' 'Ganglion', 'Wifi']")
    parser.add_argument('-p', '--port', default=None, help='Choose Cyton port or Ganglion MAC address')
    parser.add_argument('--fun', '-c', '-f', default="print_raw", help='Chosse a callback function: print_raw, lsl_stream, or osc_stream.')

    args = parser.parse_args()

    def print_raw(sample):
        print(sample.channels_data)

    callback = eval(args.fun)

    if args.board not in ['Cyton', 'CytonDaisy', 'Ganglion', 'Wifi']:
        sys.exit('No Board Selected. You should use Cyton, CytonDaisy, Ganglion, or Wifi. Try: python openbci_interface.py --board Cyton')
    elif args.board == 'Cyton':
        board = OpenBCICyton(port=args.port)
    elif args.boad == 'CytonDaisy':
        board = OpenBCICyton(port=args.port, daisy=True)
    elif args.board == 'Ganglion':
        if sys.platform.startswith("linux"):
            board = OpenBCIGanglion(mac=args.port)
        else:
            sys.exit('Currently the Ganglion Python repo only works with Linux OS.')
    else:
        board = OpenBCIWiFi()

    valid_commands = '012345678!@#$%^&*qwertyuiQWERTYUI[]pdbsvnN;-=xXDzZASFGHJKLajbs?c<>'

    while True:
        command = input('--> ')
        if str(command).lower() in ['start', 'stream']:
            print('Starting Board Stream')
            stream_thread = threading.Thread(target=board.start_stream, args=(callback, ), daemon=True)
            stream_thread.start()

        elif str(command).lower() in ['stop']:
            board.stop_stream()

        elif str(command).lower() in ['exit']:
            sys.exit()

        elif all(c in valid_commands for c in command):
            try:
                board.write_command(command)
            except:
                raise
        else:
            print('Not a valid command')
