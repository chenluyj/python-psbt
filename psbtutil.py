from psbt import (
            psbt,
            Creator,
            Updater)
from bitcoin_lib import (
    Tx,
    TxIn,
    TxOut,
)
from binascii import unhexlify
from base64 import b64encode
from bitcoinlib.encoding import addr_bech32_to_pubkeyhash

def bech32tohash160(address):
    hash160 = addr_bech32_to_pubkeyhash(address)
    return hash160

def  mkTx(listData,network,publicKey):
    # 00 目前不清楚是什么意思  可
    # 14 是hash160的长度  
    scriptPubKey_1 = unhexlify('0014') + bech32tohash160(publicKey)
    # 51 目前不清楚是什么意思  可能和原始钱包地址类型有关？
    # 20 是hash160的长度
    placeholderAddress = unhexlify('5120') + bech32tohash160("bc1pcyj5mt2q4t4py8jnur8vpxvxxchke4pzy7tdr9yvj3u3kdfgrj6sw3rzmr");
    if network == 'testnet':
        placeholderAddress = unhexlify('5120') + bech32tohash160("tb1pcyj5mt2q4t4py8jnur8vpxvxxchke4pzy7tdr9yvj3u3kdfgrj6see4dpv");
    # print(placeholderAddress)
    # print(scriptPubKey_1)
    # Inputs
    utxo_1 = unhexlify('00'*32)
    index_1 = 0
    utxo_2 = unhexlify('00'*32)
    index_2 = 1
    utxo_3 = unhexlify(listData['nftUtxo']['txHash'])
    index_3 = 0
    # Target psbt in hex
    ins = [(utxo_1, index_1),(utxo_2, index_2),(utxo_3, index_3)]
    outs = [(0,placeholderAddress),(0,placeholderAddress),(int(listData['price']), scriptPubKey_1)]
    # (int(listData['nftUtxo']['coinAmount'])
    creator= Creator(ins, outs)
    
    #添加Inputs
    _psbt = creator.serialized()
    updater = Updater(_psbt)
    
    tx_inputs = []
    for i in ins:
        tx_inputs.append(TxIn(prev_tx=i[0], prev_index=i[1], script_sig=b'', sequence=0xffffffff))
    tx_outputs = []
    ness_outs = [(0,placeholderAddress),(0,placeholderAddress),(int(listData['nftUtxo']['coinAmount']), scriptPubKey_1)]
    for i in ness_outs:
        tx_outputs.append(TxOut(amount=i[0], script_pubkey=i[1]))
    tx_obj = Tx(version=2, tx_ins=tx_inputs, tx_outs=tx_outputs, locktime=0)
    # Get a serialized version of the unsigned tx for the psbt
    serialized_tx = tx_obj.serialize()
    # Get a serialized version of the unsigned tx for the psbt
    updater.add_witness_utxo(0, serialized_tx,0)
    updater.add_witness_utxo(1, serialized_tx,1)
    updater.add_witness_utxo(2, serialized_tx,2)
    #添加Outputs
    # updater.add_output_witness_script(2,scriptPubKey_1) 
    updater.add_sighash_type(2, int.from_bytes(unhexlify('83')))
    # add out mount sdk 中为支持需要自己手动处理
    _psbt1 = updater.serialized()
    return b64encode(_psbt1).decode('utf-8')
    

def generateSignedListingPsbt(listData,network,publicKey):
    return mkTx(listData,network,publicKey)



