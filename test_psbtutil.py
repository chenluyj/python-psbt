import unittest
from base64 import b64decode
from binascii import unhexlify
from psbtutil import generateSignedListingPsbt,generateSignedBuyPsbt
class PSBTUTIL_Test(unittest.TestCase):
    def test_generateSignedListingPsbt(self):
        # https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-bitcoin/src/psbtSign.ts#L353 
        walletAddress = 'bc1qk4d47nl3nxzkfzleul5qu784ygzuhm4pn4h67p'
        publicKey = 'bc1qk4d47nl3nxzkfzleul5qu784ygzuhm4pn4h67p'
        network = 'mainnet'
        listData = {
        "nftAddress": walletAddress,
        "nftUtxo": {
            "txHash": '45c5dc378627c771cd9a4a63451a1f155f1640ba6cb4beb92d247798d052d872',
            "vout": 0,
            "coinAmount": 546,
            "rawTransaction": None
        },
        "receiveBtcAddress": walletAddress, # your btc wallet address
        "price": 10000 # total price in Satoshi unit
        }
        pyPsbt = generateSignedListingPsbt(listData,network,publicKey)
        okxPsbt ='cHNidP8BAPoCAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAP////9y2FLQmHckLbm+tGy6QBZfFR8aRWNKms1xxyeGN9zFRQAAAAAA/////wMAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctRAnAAAAAAAAFgAUtVtfT/GZhWSL+efoDnj1IgXL7qEAAAAAAAEBKwAAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUAAQErAAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQABAR8iAgAAAAAAABYAFLVbX0/xmYVki/nn6A549SIFy+6hAQMEgwAAAAAAAAA='
        self.assertEqual(pyPsbt,okxPsbt)
    
    def test_generateSignedBuyPsbt(self):
        walletAddress = 'bc1qk4d47nl3nxzkfzleul5qu784ygzuhm4pn4h67p'
        publicKey = 'bc1qk4d47nl3nxzkfzleul5qu784ygzuhm4pn4h67p'
        network = 'mainnet'
        listData = {
        "nftAddress": walletAddress,
        "nftUtxo": {
            "txHash": '45c5dc378627c771cd9a4a63451a1f155f1640ba6cb4beb92d247798d052d872',
            "vout": 0,
            "coinAmount": 546,
            "rawTransaction": None
        },
        "receiveBtcAddress": walletAddress, # your btc wallet address
        "price": 10000 # total price in Satoshi unit
        }
        pyPsbt = generateSignedListingPsbt(listData,network,publicKey)
        publicKey = unhexlify('020209aae9897b9768fa633882f563003f21c83df0bad4e7b6df73700f042ff74cc4') #压缩公钥(x)： 通过公钥可以计算出来
        singature = unhexlify('30440220473cc9619943eeafaff743bcfeb0b821a98fdbcb41763ec10e0055d283fb68e202203a3173a6423a22a34f07868582cdc8327d7cbb47061bbbcd44673faf51c5cf9883') #签名 前端可以传回来
        singPsbt = generateSignedBuyPsbt(pyPsbt,publicKey,singature)
        print(singPsbt)
        okxPsbt ='cHNidP8BAPoCAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAP////9y2FLQmHckLbm+tGy6QBZfFR8aRWNKms1xxyeGN9zFRQAAAAAA/////wMAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctRAnAAAAAAAAFgAUtVtfT/GZhWSL+efoDnj1IgXL7qEAAAAAAAEBKwAAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUAAQErAAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQABAR8iAgAAAAAAABYAFLVbX0/xmYVki/nn6A549SIFy+6hIgICCarpiXuXaPpjOIL1YwA/Icg98LrU57bfc3APBC/3TMRHMEQCIEc8yWGZQ+6vr/dDvP6wuCGpj9vLQXY+wQ4AVdKD+2jiAiA6MXOmQjoio08HhoWCzcgyfXy7RwYbu81EZz+vUcXPmIMBAwSDAAAAAAAAAA=='
        self.assertEqual(singPsbt,okxPsbt)
    
if __name__ == '__main__':
    unittest.main()
