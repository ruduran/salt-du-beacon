# -*- coding: utf-8 -*-

from __future__ import absolute_import
import logging


log = logging.getLogger(__name__)

try:
    import sh
except ImportError:
    log.error('python-sh needs to be installed')
    sh = None


__virtualname__ = 'du'


def __virtual__():
    return sh is not None


def __validate__(config):
    if isinstance(config, dict):
        return True, 'Valid config'
    else:
        error_msg = 'The configuration needs to be a dictionary'
        log.error(error_msg)
        return False, error_msg


def _get_dir_used_space(directory):
    used_space = 0

    try:
        used_space = int(sh.du(directory, s=True).split()[0])
    except:
        # TODO: Improve exception handling and error msg
        log.error('Could not obtain the disk usage')

    return used_space


def beacon(config):
    ret = []

    for directory, threshold in config.items():
        used = _get_dir_used_space(directory)

        if used >= threshold:
            ret.append({'path': directory,
                        'used': used,
                        'threshold': config[directory]})

    return ret
