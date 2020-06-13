import hashlib


# md5加密方法
def gen_md5(key):
    key_md5 = hashlib.md5()
    key_md5.update(key.encode(encoding='utf-8'))
    return key_md5.hexdigest()
