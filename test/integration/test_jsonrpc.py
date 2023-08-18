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
    genesis_hash = u'00000b6d8eb923c6b3738a509231bfc2a8943a53316d46943284ef75ba358bec'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000c859a7aa5538110a356bd4803ff55e3f85302e754e3c7994c62feb3060f'

    creds = HellarConfig.get_rpc_creds(config_text, network)
    hellard = HellarDaemon(**creds)
    assert hellard.rpc_command is not None

    assert hasattr(hellard, 'rpc_connection')

    # Hellar testnet block 0 hash == 00000c859a7aa5538110a356bd4803ff55e3f85302e754e3c7994c62feb3060f
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
