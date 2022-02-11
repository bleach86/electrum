# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

from .util import inv_dict, all_subclasses
from . import bitcoin


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


GIT_REPO_URL = "https://github.com/tecnovert/electrum"
GIT_REPO_ISSUES_URL = "https://github.com/tecnovert/electrum/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    NET_NAME: str
    TESTNET: bool
    WIF_PREFIX: int
    ADDRTYPE_P2PKH: int
    ADDRTYPE_P2SH: int
    SEGWIT_HRP: str
    BOLT11_HRP: str
    GENESIS: str
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS: int = 0
    BIP44_COIN_TYPE: int
    LN_REALM_BYTE: int

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * 2016 - 1)

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))


class ParticlMainnet(AbstractNet):

    NET_NAME = "mainnet"
    TESTNET = False
    WIF_PREFIX = 0x6c
    ADDRTYPE_P2PKH = 0x38
    ADDRTYPE_P2SH = 0x3c
    SEGWIT_HRP = "pw"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "0000ee0784c195317ac95623e22fddb8c7b8825dc3998e0bb924d66866eccf4c"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = []  # read_json('checkpoints.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 497000

    XPRV_HEADERS = {
        'standard':    0x8f1daeb8,  # XPAR
        'p2wpkh-p2sh': 0x0497347d,  # yXPA
        'p2wsh-p2sh':  0x947e7a7a,  # YXPA
        'p2wpkh':      0x04abff11,  # zXPA
        'p2wsh':       0x9934602a,  # ZXPA
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x696e82d1,  # PPAR
        'p2wpkh-p2sh': 0x04945657,  # yPPA
        'p2wsh-p2sh':  0x93d825fa,  # YPPA
        'p2wpkh':      0x04a920ea,  # zPPA
        'p2wsh':       0x988e0b6a,  # ZPPA
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 44
    LN_REALM_BYTE = 44
    LN_DNS_SEEDS = [
    ]


class ParticlTestnet(AbstractNet):

    NET_NAME = "testnet"
    TESTNET = True
    WIF_PREFIX = 0x2e
    ADDRTYPE_P2PKH = 0x76
    ADDRTYPE_P2SH = 0x7a
    SEGWIT_HRP = "tpw"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "0000594ada5310b367443ee0afd4fa3d0bbd5850ea4e33cdc7d6a904a7ec7c90"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = []  # read_json('checkpoints_testnet.json', [])

    XPRV_HEADERS = {
        'standard':    0x04889478,  # xpar
        'p2wpkh-p2sh': 0x04a052ea,  # yxpa
        'p2wsh-p2sh':  0x968f5f0a,  # Yxpa
        'p2wpkh':      0x04b51d7e,  # zxpa
        'p2wsh':       0x9b454494,  # Zxpa
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0xe1427800,  # ppar
        'p2wpkh-p2sh': 0x95e90a84,  # Yppa
        'p2wsh-p2sh':  0x049d74c4,  # yppa
        'p2wpkh':      0x04b23f58,  # zppa
        'p2wsh':       0x9a9eeff9,  # Zppa
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
        #'test.nodes.lightning.directory.',  # times out.
        #'lseed.bitcoinstats.com.',  # ignores REALM byte and returns mainnet peers...
    ]


class ParticlRegtest(ParticlTestnet):

    NET_NAME = "regtest"
    SEGWIT_HRP = "rtpw"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "6cd174536c0ada5bfa3b8fde16b98ae508fff6586f2ee24cf866867098f25907"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


class ParticlSimnet(ParticlTestnet):

    NET_NAME = "simnet"
    WIF_PREFIX = 0x64
    ADDRTYPE_P2PKH = 0x3f
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "sb"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


class ParticlSignet(ParticlTestnet):

    NET_NAME = "signet"
    BOLT11_HRP = "tbs"
    GENESIS = "00000008819873e925422c1ff0f99f7cc9bbb232af63a077a480a3633bee1ef6"
    DEFAULT_SERVERS = read_json('servers_signet.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


NETS_LIST = tuple(all_subclasses(AbstractNet))

# don't import net directly, import the module instead (so that net is singleton)
net = ParticlMainnet

def set_signet():
    global net
    net = ParticlSignet

def set_simnet():
    global net
    net = ParticlSimnet

def set_mainnet():
    global net
    net = ParticlMainnet

def set_testnet():
    global net
    net = ParticlTestnet

def set_regtest():
    global net
    net = ParticlRegtest
