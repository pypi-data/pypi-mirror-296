# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides a Spec class for specifying a connection to a BrainStem module.

A Spec instance fully describes a connection to a brainstem module. In the case of
USB based stems this is simply the serial number of the module. For TCPIP based stems
this is an IP address and TCP port.

For more information about links and the Brainstem network
see the `Acroname BrainStem Reference`_

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""
import socket
import struct

from . import _BS_C

from .defs import (
    MODEL_MTM_IOSERIAL
)

class Status(object):
    """ Status variables represent the link status possibilities for Brainstem Links.

        Status States:
            * STOPPED (0)
            * INITIALIZING (1)
            * RUNNING (2)
            * STOPPING (3)
            * SYNCING (4)
            * INVALID_LINK_STREAM (5)
            * IO_ERROR (6)
            * UNKNOWN_ERROR (7)

    """

    STOPPED = 0
    INITIALIZING = 1
    RUNNING = 2
    STOPPING = 3
    SYNCING = 4
    INVALID_LINK_STREAM = 5
    IO_ERROR = 6
    UNKNOWN_ERROR = 7


class aEtherConfig(object):
    """ aEther configuration class for configuring AETHER connection types.

        Note: If localOnly == false AND networkInterface is default (0 or LOCALHOST_IP_ADDRESS)
        it will be populated with the auto-selected interface upon successful connection.

        Attributes: 
            enabled: True: Client-Server model is used; False: Direct module control is used.
            fallback: True: If connections fails it will automatically search for network connections.
            localOnly: True: Restricts access to localhost; False: Expose device to external network.
            assignedPort: Server assigned port after successful connection.
            networkInterface: Network interface to use for connections.
    """

    def __init__(self):
        self.enabled = True
        self.fallback = True
        self.localOnly = True
        self.assignedPort = 0
        self.networkInterface = _BS_C.LOCALHOST_IP_ADDRESS

    def __str__(self):
        return "aEther Config: Enabled: %d - Fallback: %d - LocalOnly: %d - AssignedPort: %d - NetworkInterface: %d" % \
               (self.enabled, self.fallback, self.localOnly, self.assignedPort, self.networkInterface)


class Spec(object):
    """ Spec class for specifying connection details

        Instances of Spec represent the connection details for a brainstem link.
        The Spec class also contains constants representing the possible transport
        types for BrainStem modules.

        args:
            transport (int): One of USB, TCPIP, SERIAL or AETHER.
            serial_number (int): The module serial number.
            module: The module address on the Brainstem network.
            model: The device model number of the Brainstem module.
            **keywords: For TCPIP, SERIAL and AETHER connections. The possibilities are,

                * ip_address: (int/str) The IPV4 address for a TCPIP/AETHER connection type.
                * ip_port: (int/str) The port for a TCPIP/AETHER connection type.
                * port: (str) The serial port for a SERIAL connection type.
                * baudrate: (int/str) The baudrate for a SERIAL connection type.

    """
    INVALID = 0                         #: INVALID Undefined transport type.
    USB = 1                             #: USB transport type.
    TCPIP = 2                           #: TCPIP transport type.
    SERIAL = 3                          #: SERIAL transport type.
    AETHER = 4                          #: AETHER transport type.

    def __init__(self, transport, serial_number, module, model, **keywords):

        self.transport = transport
        self.serial_number = serial_number
        self.module = module

        # Model was added in 2.2.0  This adds legacy support
        if model == 2:
            self.model = MODEL_MTM_IOSERIAL
        else:
            self.model = model

        for key in keywords.keys():
            if key == 'ip_address':
                if isinstance(keywords[key], int):
                    self.ip_address = keywords[key]
                else:
                    try:
                        self.ip_address = socket.inet_aton(keywords[key])
                    except socket.error:
                        raise ValueError("Failed to convert ip_address key ", keywords[key])

            elif key == 'ip_port':
                if isinstance(keywords[key], int):
                    self.ip_port = keywords[key]
                else:
                    try:
                        self.ip_port = int(keywords[key])
                    except ValueError:
                        raise ValueError("Failed to convert ip_port key ", keywords[key])

            elif key == 'port':
                if isinstance(keywords[key], str):
                    self.port = keywords[key]
                else:
                    try:
                        #This is probably a bad choice as it will ALWAYS succeed.
                        self.port = str(keywords[key])
                    except ValueError:
                        #This should never happen because every type in python can be converted to a string
                        raise ValueError("Failed to convert port key ", keywords[key])

            elif key == 'baudrate':
                if isinstance(keywords[key], int):
                    self.baudrate = keywords[key]
                else:
                    try:
                        self.baudrate = int(keywords[key])
                    except ValueError:
                        raise ValueError("Failed to convert baudrate key ", keywords[key])

            else:
                raise KeyError("Unknown keyword in Spec ", key)


    def __str__(self):
        type_string = "USB"
        if self.transport == Spec.TCPIP:
            type_string = "TCPIP"
        elif self.transport == Spec.SERIAL:
            type_string = "SERIAL"
        elif self.transport == Spec.AETHER:
            type_string = "AETHER"

        addr, port = ('', '')
        if hasattr(self, 'ip_address'):
            addr = ", IP Address: %s" % socket.inet_ntoa(struct.pack('!I', socket.htonl(self.ip_address)))
        if hasattr(self, 'ip_port'):
            port = ", IP Port: %d" % self.ip_port
        if hasattr(self, 'port'):
            port += ", Serial Port: %s" % self.port
        if hasattr(self, 'baudrate'):
            port += ", Baudrate: %d" % self.baudrate
        return 'Model: %s LinkType: %s(serial: %08X%s%s)' % (self.model, type_string, self.serial_number, addr, port)
