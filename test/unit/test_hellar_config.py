import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from hellar_config import HellarConfig


@pytest.fixture
def hellar_conf(**kwargs):
    defaults = {
        'rpcuser': 'hellarrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 27788,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    hellar_config = hellar_conf()
    creds = HellarConfig.get_rpc_creds(hellar_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'hellarrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 27788

    hellar_config = hellar_conf(rpcpassword='s00pers33kr1t', rpcport=7788)
    creds = HellarConfig.get_rpc_creds(hellar_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'hellarrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 7788

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', hellar_conf(), re.M)
    creds = HellarConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'hellarrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 27782


# ensure hellar network (mainnet, testnet) matches that specified in config
# requires running hellard on whatever port specified...
#
# This is more of a hellard/jsonrpc test than a config test...
