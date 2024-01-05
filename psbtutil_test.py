import unittest
from psbtutil import generateSignedListingPsbt
class PSBTUTIL_Test(unittest.TestCase):
    def test_generateSignedListingPsbt(self):
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
    
if __name__ == '__main__':
    unittest.main()
