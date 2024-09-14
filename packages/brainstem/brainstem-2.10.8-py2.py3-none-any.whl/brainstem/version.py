# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

""" Provides version access utilities. """

from . import _BS_C, ffi


def get_version_string(packed_version=None):
    """ Returns the library version as a string

        args:
            packed_version (int(Optional)): If version is provided, it is unpacked
                                            and presented as the version string.
                                            Most useful for printing the firmware
                                            version currently installed on a module.
    """
    if not packed_version:
        return 'Brainstem library version: ' + str(ffi.string(_BS_C.aVersion_GetString()))
    else:
        return 'Brainstem version: %d.%d.%d' % unpack_version(packed_version)


def unpack_version(packed_version):
    """ Returns the library version as a 3-tuple (major, minor, patch)

        args:
            packed_version (int(Optional)): The packed version number.
    """
    major = _BS_C.aVersion_ParseMajor(packed_version)
    minor = _BS_C.aVersion_ParseMinor(packed_version)
    patch = _BS_C.aVersion_ParsePatch(packed_version)
    return major, minor, patch
