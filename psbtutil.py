from psbt import (
            Creator,
            Updater,
            Signer)
from bitcoin_lib import (
    Tx,
    TxIn,
    TxOut,
)
from binascii import unhexlify
from base64 import b64encode,b64decode
from bitcoinlib.encoding import addr_bech32_to_pubkeyhash

SELLER_INDEX = 2;
DUMMY_AMOUNT = 600;
DUST_OUTPUT_LIMIT = 546;


def bech32tohash160(address):
    hash160 = addr_bech32_to_pubkeyhash(address)
    return len(hash160).to_bytes(length=1,byteorder='little') + hash160

def  mkTx(listData,network,publicKey):
    # 00 目前不清楚是什么意思 
    scriptPubKey_1 = unhexlify('00') + bech32tohash160(publicKey)
    # 51 目前不清楚是什么意思  
    placeholderAddress = unhexlify('51') + bech32tohash160("bc1pcyj5mt2q4t4py8jnur8vpxvxxchke4pzy7tdr9yvj3u3kdfgrj6sw3rzmr");
    if network == 'testnet':
        placeholderAddress = unhexlify('51') + bech32tohash160("tb1pcyj5mt2q4t4py8jnur8vpxvxxchke4pzy7tdr9yvj3u3kdfgrj6see4dpv");
    # Global Tx
    utxo_placeholder = unhexlify('00'*32)
    index_1 = 0
    index_2 = 1
    utxo_3 = unhexlify(listData['nftUtxo']['txHash'])
    index_3 = 0
    ins = [(utxo_placeholder, index_1),(utxo_placeholder, index_2),(utxo_3, index_3)]
    outs = [(0,placeholderAddress),(0,placeholderAddress),(int(listData['price']), scriptPubKey_1)]
    creator= Creator(ins, outs)
    
    #添加Inputs
    _psbt = creator.serialized()
    updater = Updater(_psbt)
    
    tx_inputs = []
    for i in ins:
        tx_inputs.append(TxIn(prev_tx=i[0], prev_index=i[1], script_sig=b'', sequence=0xffffffff))
    tx_outputs = []
    ness_outs = [(0,placeholderAddress),(0,placeholderAddress),(int(DUST_OUTPUT_LIMIT), scriptPubKey_1)]
    for i in ness_outs:
        tx_outputs.append(TxOut(amount=i[0], script_pubkey=i[1]))
    tx_obj = Tx(version=2, tx_ins=tx_inputs, tx_outs=tx_outputs, locktime=0)
    # Get a serialized version of the unsigned tx for the psbt
    serialized_tx = tx_obj.serialize()
    # Get a serialized version of the unsigned tx for the psbt
    updater.add_witness_utxo(0, serialized_tx,0)
    updater.add_witness_utxo(1, serialized_tx,1)
    updater.add_witness_utxo(SELLER_INDEX, serialized_tx,SELLER_INDEX)
    # updater.add_output_witness_script(2,scriptPubKey_1) 
    # 参考okx的SDK 设置的默认值
    updater.add_sighash_type(2, int.from_bytes(unhexlify('83')))
    
    _psbt1 = updater.serialized()
    return b64encode(_psbt1).decode('utf-8')

def generateSignedListingPsbt(listData,network,publicKey):
    return mkTx(listData,network,publicKey)


def generateSignedBuyPsbt(psbt,publickey,singature):
    psbt_bytes= b64decode(psbt)
    updater = Updater(psbt_bytes)
    updater.add_public_signing_key(2,singature,publickey)
    _psbt1 = updater.serialized()
    return b64encode(_psbt1).decode('utf-8')
    