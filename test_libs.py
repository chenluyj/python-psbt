#!/usr/bin/env python
from base64 import b64decode
from binascii import unhexlify
from btclib.psbt import Psbt
from io import BytesIO
from base64 import b64encode
from bitcoinlib.encoding import addr_bech32_to_pubkeyhash
from psbtutil import signPsbt
from bitcoin_lib import (
            hash160,
            read_varint,
            encode_varint,
            int_to_little_endian,
            little_endian_to_int
             )
from psbt import (
            psbt,
            Creator,
            Updater,
            Signer,
            Combiner,
            Input_Finalizer,
            Transaction_Extractor
            )

def TransactionParse(s):
    if isinstance(s, str):
        s = BytesIO(unhexlify(s))
    elif isinstance(s, bytes):
        s = BytesIO(s)
    version = s.read(4)
    print('Tx')
    print('===========')
    print('version: ', version.hex())
    utxo_count = read_varint(s)
    for i in range(utxo_count):
        _utxo = s.read(37)
        Sequence = s.read(4)
        print(i,'utxo: ', _utxo.hex(),Sequence.hex())
    output_count = read_varint(s)
    for i in range(output_count):
        # value = struct.unpack('<HHHH',s.read(8))
        value = little_endian_to_int(s.read(8))
        adderlen = read_varint(s)
        adderss = s.read(adderlen)
        print(i,'output: ', f'{int_to_little_endian(value,8).hex()+ int.to_bytes(adderlen).hex() +adderss.hex()} => ({value},{adderss.hex()})')
    
# 将Bech32地址转换为Hash160格式
def bech32tohash160(address):
    # address = "bc1qk4d47nl3nxzkfzleul5qu784ygzuhm4pn4h67p"
    hash160 = addr_bech32_to_pubkeyhash(address)
    _h160 = hash160.hex()
    print(len(_h160),_h160)
  
def commParse(psbtstr):
    psbt_byte = unhexlify(psbtstr)
    # pbst_len = len(psbt_byte)
    # print('unsign_psbt: \n', psbt_byte.hex(),pbst_len)
    psbtInfo = psbt.parse(BytesIO(psbt_byte))
    print(psbtInfo)
    psbtInfo = Psbt.parse(BytesIO(psbt_byte))
    tx_byte = psbtInfo.tx.serialize(True)
    # print('Tx:',tx_byte.hex())
    TransactionParse(tx_byte)
    print(psbtInfo.serialize(False).hex() == psbt)
    
def unisatBuyParse():
    print('*'*100 + 'unisatBuy' + '*'*50)
    # unsignpsbt = '70736274ff0100fdb50102000000056c5eee2de48c93308752b7b8eefc52e280187e41ef499babedcd4869e2f38c2f0400000000ffffffff6c5eee2de48c93308752b7b8eefc52e280187e41ef499babedcd4869e2f38c2f0500000000ffffffff4ac14365d471e04596e8131ebb910d3af0452c1503527d8eab04a0ea667988170000000000ffffffffb90e930c13deaa0372d6debf744082fb083999cadfa88c5c2e6427ddbced55a50500000000ffffffff6c5eee2de48c93308752b7b8eefc52e280187e41ef499babedcd4869e2f38c2f0000000000ffffffff065802000000000000160014a896b19b43b44caf03e8d9e08bdcd9dbf5f67fb922020000000000002251201736c0d8b79a3f81a6eaf111561e122c73e872fda63621db04ee7332e48b25ba20a1070000000000225120f4b429a215d43ff1b3f4f6a704c35c487d4dd28ad7d0581702d447fcba79d1637b470400000000002251201736c0d8b79a3f81a6eaf111561e122c73e872fda63621db04ee7332e48b25ba2c01000000000000160014a896b19b43b44caf03e8d9e08bdcd9dbf5f67fb92c01000000000000160014a896b19b43b44caf03e8d9e08bdcd9dbf5f67fb9000000000001011f2c01000000000000160014a896b19b43b44caf03e8d9e08bdcd9dbf5f67fb90001011f2c01000000000000160014a896b19b43b44caf03e8d9e08bdcd9dbf5f67fb90001012b2202000000000000225120f4b429a215d43ff1b3f4f6a704c35c487d4dd28ad7d0581702d447fcba79d1630103048300000001172002045f237ce214f83acf0691e9ff3a81280617fcaf336ffc6605ea6c060b9bc60001012b22550c00000000002251201736c0d8b79a3f81a6eaf111561e122c73e872fda63621db04ee7332e48b25ba011720b1e2a8839318e80cbd14f66737ebcc5fa82e5da03166e4593dc48f178caa04c80001011f5802000000000000160014a896b19b43b44caf03e8d9e08bdcd9dbf5f67fb900000000000000'
    unsignpsbt = '70736274ff0100fdaa010200000005b4e7414d0a9f706293d39fb493ac60e50cc16c25a1d724a4f58537b6bfa689d30400000000ffffffffb4e7414d0a9f706293d39fb493ac60e50cc16c25a1d724a4f58537b6bfa689d30500000000ffffffff624b2c111b218b2922446a1d7a2ff0b0426c86321a3834b50af374e3a20cef8f0000000000ffffffff88a8c2f77fb3e3f70bc03560eef877e1a20652b2c207af544c51422ec6c080460200000000ffffffffb4e7414d0a9f706293d39fb493ac60e50cc16c25a1d724a4f58537b6bfa689d30000000000ffffffff065802000000000000160014f1d1ee30916f7719060889901fbafed499b515d522020000000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d138800f915000000000017a914e054a8a155c20bf6f88c760edee34211ece5bfb8877c0f0500000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d13882c01000000000000160014f1d1ee30916f7719060889901fbafed499b515d52c01000000000000160014f1d1ee30916f7719060889901fbafed499b515d5000000000001011f2c01000000000000160014f1d1ee30916f7719060889901fbafed499b515d50001011f2c01000000000000160014f1d1ee30916f7719060889901fbafed499b515d50001012b22020000000000002251205ab21c113416a5cbea9f9f1977b8005668db955cec31ef59b928e024cb2ca7f9010304830000000117205294ea6ada5ab436db6dc81ff108786c7ec83d8702d6db101d0f03c2ef9e00ff0001012b40771b00000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d13880117206ce485ac1ff92e8279b72d714a6f5a98e2079f76bc4e6b273f62535f4f87734b0001011f5802000000000000160014f1d1ee30916f7719060889901fbafed499b515d500000000000000'
    commParse(unsignpsbt)

def unisatSellParse():
    print('*'*100 + 'unisatSell' + '*'*50)
    unsignpsbt = '70736274ff0100f4020000000300000000000000000000000000000000000000000000000000000000000000000000000000ffffffff00000000000000000000000000000000000000000000000000000000000000000100000000ffffffff17866fb4d404a629a517a754af6679164a400fee730b1fb568b8b884dd123b290000000000ffffffff0300000000000000001976a914000000000000000000000000000000000000000088ac00000000000000001976a914000000000000000000000000000000000000000088ac60e31600000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d1388000000000001011f0000000000000000160014ae47938f7acd1623e6e10e1ebcc33c2a7cb6e30d0001011f0000000000000000160014ae47938f7acd1623e6e10e1ebcc33c2a7cb6e30d0001012b22020000000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d1388010304830000000117206ce485ac1ff92e8279b72d714a6f5a98e2079f76bc4e6b273f62535f4f87734b00000000'   
    commParse(unsignpsbt)
    
def okxParse():
    print('*'*100 + 'okxParse' + '*'*50)
    unsignedPsbt  = 'cHNidP8BAPoCAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAP////9y2FLQmHckLbm+tGy6QBZfFR8aRWNKms1xxyeGN9zFRQAAAAAA/////wMAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctRAnAAAAAAAAFgAUtVtfT/GZhWSL+efoDnj1IgXL7qEAAAAAAAEBKwAAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUAAQErAAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQABAR8iAgAAAAAAABYAFLVbX0/xmYVki/nn6A549SIFy+6hAQMEgwAAAAAAAAA='
    unsignedPsbt = b64decode(unsignedPsbt).hex()
    commParse(unsignedPsbt)    

def okxSDKsign():
    print('*'*100 + 'okxSDKsign' + '*'*50)
    unsignedPsbt = 'cHNidP8BAPoCAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAP////9y2FLQmHckLbm+tGy6QBZfFR8aRWNKms1xxyeGN9zFRQAAAAAA/////wMAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctRAnAAAAAAAAFgAUtVtfT/GZhWSL+efoDnj1IgXL7qEAAAAAAAEBKwAAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUAAQErAAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQABAR8iAgAAAAAAABYAFLVbX0/xmYVki/nn6A549SIFy+6hIgICCarpiXuXaPpjOIL1YwA/Icg98LrU57bfc3APBC/3TMRHMEQCIEc8yWGZQ+6vr/dDvP6wuCGpj9vLQXY+wQ4AVdKD+2jiAiA6MXOmQjoio08HhoWCzcgyfXy7RwYbu81EZz+vUcXPmIMBAwSDAAAAAAAAAA=='
    unsignedPsbt = b64decode(unsignedPsbt).hex()
    commParse(unsignedPsbt)   

def okxBuy():
    print('*'*100 + 'okxSDKBuysign' + '*'*50)
    unsignedPsbt = 'cHNidP8BAP0GAQIAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAA/////+Kx5JxQFqXQZan42i6zueN4noyQPFzWfW7dCuBTdWJBAAAAAAD/////AwAAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy10HIDAAAAAAAiUSB+lR+coe0b0LuGwSr6otG161wMvnxg6d+Uoy6GhOiVMAAAAAAAAQErAAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQABASsAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AAEBKyICAAAAAAAAIlEgfpUfnKHtG9C7hsEq+qLRtetcDL58YOnflKMuhoTolTABAwSDAAAAARcgiBjYprWX3s+7yUflpOgtLpnKg57LkmWp0jwFUrMwClsAAAAA'
    unsignedPsbt = b64decode(unsignedPsbt).hex()
    commParse(unsignedPsbt)   

if __name__ == '__main__':
    '''
    帮助理解psbt结构
    '''
    # unisatSellParse()
    unisatBuyParse()
    okxParse()
    # okxSDKsign()
    okxBuy()

