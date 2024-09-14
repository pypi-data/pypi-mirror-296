import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class DecryptLibrary:

    @staticmethod
    def get_decrypted_string(enc, key):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(enc), 16)
        str_as_decrypted = decrypted.decode("utf-8", "ignore")
        return str_as_decrypted

    # print(get_decrypted_message('cZzgHM0MrP1J9eANiWmFORra0pOnt2se+vcaoTmSFoo=', '3As%UX*w6f5xv5*!'))
