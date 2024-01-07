from btclib.psbt import Psbt
from base64 import b64decode

def test_psbt():
    # 你的 PSBT 数据
    psbt_data = "cHNidP8BAPoCAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAP////9y2FLQmHckLbm+tGy6QBZfFR8aRWNKms1xxyeGN9zFRQAAAAAA/////wMAAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctRAnAAAAAAAAFgAUtVtfT/GZhWSL+efoDnj1IgXL7qEAAAAAAAEBKwAAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUAAQErAAAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQABAR8iAgAAAAAAABYAFLVbX0/xmYVki/nn6A549SIFy+6hAQMEgwAAAAAAAAA="
    phex = bytes.fromhex(b64decode(psbt_data).hex()).hex()
    # 加载 PSBT
    psbt = Psbt.parse(phex)
    Psbt()
    signed_psbt = psbt.serialize()
    ePsbt = signed_psbt.hex()
    print(ePsbt == phex)
    
if __name__ == '__main__':
    test_psbt()