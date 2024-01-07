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
    segwitMarker = s.read(1)
    SegwitFlag = s.read(1)
    print('Tx')
    print('===========')
    print('version: ', version.hex())
    print('segwitMarker: ', segwitMarker.hex())
    print('SegwitFlag: ', SegwitFlag.hex())
    inputs_count = read_varint(s)
    print('inputs_count:',inputs_count)
    for i in range(inputs_count):
        prev_hash = s.read(32)
        prev_index = s.read(4)
        scriptSig_len= read_varint(s)
        scriptSig = s.read(scriptSig_len)
        Sequence = s.read(4)
        print(i,'prev_hash: ', prev_hash.hex(),prev_index.hex(),scriptSig.hex(),Sequence.hex())
    output_count = read_varint(s)
    print('output_count:',output_count)
    for i in range(output_count):
        # value = struct.unpack('<HHHH',s.read(8))
        value = little_endian_to_int(s.read(8))
        adderlen = read_varint(s)
        adderss = s.read(adderlen)
        print(i,'output: ', f'{int_to_little_endian(value,8).hex()+ int.to_bytes(adderlen).hex() +adderss.hex()} => ({value},{adderss.hex()})')
    witness_len = read_varint(s)
    print('witness_len:',witness_len)
    if witness_len != 0:
        for i in range(inputs_count):
            witness = s.read(witness_len)
            print(i,'witness: ', witness.hex())
    scriptWitness_count = read_varint(s)
    print('scriptWitness_count:',scriptWitness_count)
    _o00 = s.read(1) #不清楚是什么意思
    for i in range(scriptWitness_count-1): # TODO 硬编码的 不明白 因为只有3witness
        script_len = read_varint(s)
        script = s.read(script_len)
        print('scriptWitness: ', hex(script_len)[2:],script.hex())
    locktime = s.read(4)
    print('locktime: ', locktime.hex())
    
def globalParse(s):
    if isinstance(s, str):
        s = BytesIO(unhexlify(s))
    elif isinstance(s, bytes):
        s = BytesIO(s)
    version = s.read(4)
    print('Global Tx')
    print('===========')
    print('version: ', version.hex())
    utxo_count = read_varint(s)
    for i in range(utxo_count):
        _utxo = s.read(37)
        Sequence = s.read(4)
        print(i,'utxo: ', _utxo.hex(),Sequence.hex())
    output_count = read_varint(s)
    print('output_count:',output_count)
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
    globalParse(tx_byte)
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

def test_finalizer():
    want = unhexlify('70736274ff01009a020000000258e87a21b56daf0c23be8e7070456c336f7cbaa5c8757924f545887bb2abdd750000000000ffffffff838d0427d0ec650a68aa46bb0b098aea4422c071b2ca78352a077959d07cea1d0100000000ffffffff0270aaf00800000000160014d85c2b71d0060b09c9886aeb815e50991dda124d00e1f5050000000016001400aea9a2e5f0f876a588df5546e8742d1d87008f00000000000100bb0200000001aad73931018bd25f84ae400b68848be09db706eac2ac18298babee71ab656f8b0000000048473044022058f6fc7c6a33e1b31548d481c826c015bd30135aad42cd67790dab66d2ad243b02204a1ced2604c6735b6393e5b41691dd78b00f0c5942fb9f751856faa938157dba01feffffff0280f0fa020000000017a9140fb9463421696b82c833af241c78c17ddbde493487d0f20a270100000017a91429ca74f8a08f81999428185c97b5d852e4063f6187650000000107da00473044022074018ad4180097b873323c0015720b3684cc8123891048e7dbcd9b55ad679c99022073d369b740e3eb53dcefa33823c8070514ca55a7dd9544f157c167913261118c01483045022100f61038b308dc1da865a34852746f015772934208c6d24454393cd99bdf2217770220056e675a675a6d0a02b85b14e5e29074d8a25a9b5760bea2816f661910a006ea01475221029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f2102dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d752ae0001012000c2eb0b0000000017a914b7f5faf40e3d40a5a459b1db3535f2b72fa921e8870107232200208c2353173743b595dfb4a07b72ba8e42e3797da74e87fe7d9d7497e3b20289030108da0400473044022062eb7a556107a7c73f45ac4ab5a1dddf6f7075fb1275969a7f383efff784bcb202200c05dbb7470dbf2f08557dd356c7325c1ed30913e996cd3840945db12228da5f01473044022065f45ba5998b59a27ffe1a7bed016af1f1f90d54b3aa8f7450aa5f56a25103bd02207f724703ad1edb96680b284b56d4ffcb88f7fb759eabbe08aa30f29b851383d20147522103089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc21023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e7352ae00220203a9a4c37f5996d3aa25dbac6b570af0650394492942460b354753ed9eeca5877110d90c6a4f000000800000008004000080002202027f6399757d2eff55a136ad02c684b1838b6556e5f1b6b34282a94b6b5005109610d90c6a4f00000080000000800500008000')
    # test_finalizer.make_file()
    _psbt = '70736274ff01009a020000000258e87a21b56daf0c23be8e7070456c336f7cbaa5c8757924f545887bb2abdd750000000000ffffffff838d0427d0ec650a68aa46bb0b098aea4422c071b2ca78352a077959d07cea1d0100000000ffffffff0270aaf00800000000160014d85c2b71d0060b09c9886aeb815e50991dda124d00e1f5050000000016001400aea9a2e5f0f876a588df5546e8742d1d87008f00000000000100bb0200000001aad73931018bd25f84ae400b68848be09db706eac2ac18298babee71ab656f8b0000000048473044022058f6fc7c6a33e1b31548d481c826c015bd30135aad42cd67790dab66d2ad243b02204a1ced2604c6735b6393e5b41691dd78b00f0c5942fb9f751856faa938157dba01feffffff0280f0fa020000000017a9140fb9463421696b82c833af241c78c17ddbde493487d0f20a270100000017a91429ca74f8a08f81999428185c97b5d852e4063f6187650000002202029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f473044022074018ad4180097b873323c0015720b3684cc8123891048e7dbcd9b55ad679c99022073d369b740e3eb53dcefa33823c8070514ca55a7dd9544f157c167913261118c01220202dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d7483045022100f61038b308dc1da865a34852746f015772934208c6d24454393cd99bdf2217770220056e675a675a6d0a02b85b14e5e29074d8a25a9b5760bea2816f661910a006ea01010304010000000104475221029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f2102dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d752ae2206029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f10d90c6a4f000000800000008000000080220602dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d710d90c6a4f0000008000000080010000800001012000c2eb0b0000000017a914b7f5faf40e3d40a5a459b1db3535f2b72fa921e8872202023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e73473044022065f45ba5998b59a27ffe1a7bed016af1f1f90d54b3aa8f7450aa5f56a25103bd02207f724703ad1edb96680b284b56d4ffcb88f7fb759eabbe08aa30f29b851383d201220203089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc473044022062eb7a556107a7c73f45ac4ab5a1dddf6f7075fb1275969a7f383efff784bcb202200c05dbb7470dbf2f08557dd356c7325c1ed30913e996cd3840945db12228da5f010103040100000001042200208c2353173743b595dfb4a07b72ba8e42e3797da74e87fe7d9d7497e3b2028903010547522103089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc21023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e7352ae2206023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e7310d90c6a4f000000800000008003000080220603089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc10d90c6a4f00000080000000800200008000220203a9a4c37f5996d3aa25dbac6b570af0650394492942460b354753ed9eeca5877110d90c6a4f000000800000008004000080002202027f6399757d2eff55a136ad02c684b1838b6556e5f1b6b34282a94b6b5005109610d90c6a4f00000080000000800500008000'
    commParse(_psbt)   
    print('*'*100 + 'test_finalizer' + '*'*50)
    raw_psbt = unhexlify('70736274ff01009a020000000258e87a21b56daf0c23be8e7070456c336f7cbaa5c8757924f545887bb2abdd750000000000ffffffff838d0427d0ec650a68aa46bb0b098aea4422c071b2ca78352a077959d07cea1d0100000000ffffffff0270aaf00800000000160014d85c2b71d0060b09c9886aeb815e50991dda124d00e1f5050000000016001400aea9a2e5f0f876a588df5546e8742d1d87008f00000000000100bb0200000001aad73931018bd25f84ae400b68848be09db706eac2ac18298babee71ab656f8b0000000048473044022058f6fc7c6a33e1b31548d481c826c015bd30135aad42cd67790dab66d2ad243b02204a1ced2604c6735b6393e5b41691dd78b00f0c5942fb9f751856faa938157dba01feffffff0280f0fa020000000017a9140fb9463421696b82c833af241c78c17ddbde493487d0f20a270100000017a91429ca74f8a08f81999428185c97b5d852e4063f6187650000002202029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f473044022074018ad4180097b873323c0015720b3684cc8123891048e7dbcd9b55ad679c99022073d369b740e3eb53dcefa33823c8070514ca55a7dd9544f157c167913261118c01220202dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d7483045022100f61038b308dc1da865a34852746f015772934208c6d24454393cd99bdf2217770220056e675a675a6d0a02b85b14e5e29074d8a25a9b5760bea2816f661910a006ea01010304010000000104475221029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f2102dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d752ae2206029583bf39ae0a609747ad199addd634fa6108559d6c5cd39b4c2183f1ab96e07f10d90c6a4f000000800000008000000080220602dab61ff49a14db6a7d02b0cd1fbb78fc4b18312b5b4e54dae4dba2fbfef536d710d90c6a4f0000008000000080010000800001012000c2eb0b0000000017a914b7f5faf40e3d40a5a459b1db3535f2b72fa921e8872202023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e73473044022065f45ba5998b59a27ffe1a7bed016af1f1f90d54b3aa8f7450aa5f56a25103bd02207f724703ad1edb96680b284b56d4ffcb88f7fb759eabbe08aa30f29b851383d201220203089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc473044022062eb7a556107a7c73f45ac4ab5a1dddf6f7075fb1275969a7f383efff784bcb202200c05dbb7470dbf2f08557dd356c7325c1ed30913e996cd3840945db12228da5f010103040100000001042200208c2353173743b595dfb4a07b72ba8e42e3797da74e87fe7d9d7497e3b2028903010547522103089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc21023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e7352ae2206023add904f3d6dcf59ddb906b0dee23529b7ffb9ed50e5e86151926860221f0e7310d90c6a4f000000800000008003000080220603089dc10c7ac6db54f91329af617333db388cead0c231f723379d1b99030b02dc10d90c6a4f00000080000000800200008000220203a9a4c37f5996d3aa25dbac6b570af0650394492942460b354753ed9eeca5877110d90c6a4f000000800000008004000080002202027f6399757d2eff55a136ad02c684b1838b6556e5f1b6b34282a94b6b5005109610d90c6a4f00000080000000800500008000')    
    test_finalizer = Input_Finalizer(raw_psbt)
    result = test_finalizer.serialized()
    # print(result.hex())   
    commParse(result.hex())  

def test():
    _psbt = '70736274ff0100f4020000000300000000000000000000000000000000000000000000000000000000000000000000000000ffffffff00000000000000000000000000000000000000000000000000000000000000000100000000ffffffff17866fb4d404a629a517a754af6679164a400fee730b1fb568b8b884dd123b290000000000ffffffff0300000000000000001976a914000000000000000000000000000000000000000088ac00000000000000001976a914000000000000000000000000000000000000000088ac60e31600000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d1388000000000001011f0000000000000000160014ae47938f7acd1623e6e10e1ebcc33c2a7cb6e30d0001011f0000000000000000160014ae47938f7acd1623e6e10e1ebcc33c2a7cb6e30d0001012b22020000000000002251207eb2fe599d8af47f6be302c9c035da91cc16c93a3730acde44d3839ef02d1388010304830000000117206ce485ac1ff92e8279b72d714a6f5a98e2079f76bc4e6b273f62535f4f87734b00000000'    
    commParse(_psbt)  
if __name__ == '__main__':
    '''
    帮助理解psbt结构
    '''
    
    unisatSellParse()
    # unisatBuyParse()
    # okxParse()
    # okxSDKsign()
    # okxBuy()
    # test_finalizer()
    # test()


