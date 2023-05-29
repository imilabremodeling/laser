import socket
#import prettytable as pt
import os, binascii
import random
import time
import threading
from AS import check_device

# user would trigger DB to do authentication automatically on the website.
# user press the button of "CNC Agent" on the website.
# then DB would connect to CNC agent to get data from CNC and store it in DB.
# this .py is used to get trigger flag from website and do client_func which does the step of registeration and authentication.

check_device()

