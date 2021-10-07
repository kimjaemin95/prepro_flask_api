'''
MAM API DOCS
    # https://documenter.getpostman.com/view/5025112/TVYAfLRw#337b9241-bb71-4862-89d1-6a78e578e094
Conf :
    # Python3.7.2
    # OS : CenOS(Linux)
Lib : 
    # pip install --upgrade pip
    # pip install pycryptodome (for linux)
    # pip install pycryptodomex (for window)
Crypto :
    # AES256
    # ECB Mode
    # padding : ZeroPadding -> pad_asc = chr(0), unpad_asc = b'\x00'
    # CharSet : UTF-8
Key : 
    # 92841692dee96c82482c180b2408a866
'''


from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


BLOCK_SIZE = 16  # Bytes
pad_asc = chr(0)
unpad_asc = b'\x00'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * pad_asc
unpad = lambda s: s.replace(unpad_asc, b'')
 
class AESCipher:
    """
    Usage:
        c = AESCipher('key').encrypt('message')
        m = AESCipher('key').decrypt(c)
    """

    def __init__(self, key):
        self.key = bytes(key, encoding='utf-8')

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw.encode('utf8')))

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')

key = '92841692dee96c82482c180b2408a866'
data = '{"userId":"admin","password":"p@ssw0rd!"}'

ob = AESCipher(key)
enc = ob.encrypt(data)
dec = ob.decrypt(enc)
print('Encryt :', enc, len(enc), type(enc))
print('Decrypt :', dec, len(dec), type(dec))
print('MAM API Login encrypted :', enc.decode('utf-8'))


