import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from hellard import HellarDaemon
from hellar_config import HellarConfig


def test_hellard():
    config_text = HellarConfig.slurp_config_file(config.hellar_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000fa67255a934520d6ff572828aa339af437d78ce6e6e6f4b2bd9ad30a0b9'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000b40bd778a9d4c0d35b674f7d09fec42e6c38bd3695e73a72b16519fcfe7'

    creds = HellarConfig.get_rpc_creds(config_text, network)
    hellard = HellarDaemon(**creds)
    assert hellard.rpc_command is not None

    assert hasattr(hellard, 'rpc_connection')

    # Hellar testnet block 0 hash == 00000b40bd778a9d4c0d35b674f7d09fec42e6c38bd3695e73a72b16519fcfe7
    # test commands without arguments
    info = hellard.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert hellard.rpc_command('getblockhash', 0) == genesis_hash
