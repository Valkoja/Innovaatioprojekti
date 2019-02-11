# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# 01_canlib_buson_off.py
from canlib import canlib
from canlib.canlib import ChannelData

channel = 0
chd = canlib.ChannelData(channel)
print("CANlib version: v{}".format(chd.dll_product_version))
print("canlib dll version: v{}".format(chd.dll_file_version))
print("Using channel: {ch}, EAN: {ean}".
   format(ch=chd.device_name, ean=chd.card_upc_no))

ch1 = canlib.openChannel(channel, canlib.canOPEN_ACCEPT_VIRTUAL)
ch1.setBusOutputControl(canlib.canDRIVER_NORMAL)
ch1.setBusParams(canlib.canBITRATE_1M)
ch1.busOn()
ch1.busOff()