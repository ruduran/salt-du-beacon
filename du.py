# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    import sh
    SH_AVAILABLE = True
except ImportError:
    SH_AVAILABLE = False

__virtualname__ = 'du'


def __virtual__():
    if SH_AVAILABLE is False:
        return False, "python-sh needs to be installed"
    else:
        return __virtualname__


def __validate__(config):
    if isinstance(config, dict):
        return True, "Valid config"
    else:
        return False, 'A dict is required'


def beacon(config):
    ret = []

    for directory in config.keys():
        try:
            used = int(sh.du(directory, s=True).split()[0])
            threshold = config[directory]

            if used >= threshold:
                ret.append({'path': directory, 'used': used, 'threshold': config[directory]})
        except:
            ret.append({'path': directory, 'error': 'Could not obtain the disk usage'})

    return ret
