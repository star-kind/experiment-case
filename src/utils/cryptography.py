import hashlib
import uuid
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad, unpad  
import base64  
import records

def get_salt():
    # 获取UUID
    unique_id = uuid.uuid4()
    
    # 进行md5加密
    md5 = hashlib.md5()
    md5.update(str(unique_id).encode('utf-8'))
    encrypted_string = md5.hexdigest()
    
    salt_str=encrypted_string.replace("-","")
    salt=salt_str[:16] # 截取字符串的0-16位字符
    
    records.type_msg(True_salt = salt)
    return salt

# private_key 的长度必须为16
# 加密，返回加密后的密文
def aes_encrypt(private_key: str, personal_word: str) -> str:  
    # 检查 private_key 的长度是否为 16、24 或 32 字节，如果不是，则抛出 ValueError 异常 
    if len(private_key) not in [16, 24, 32]:  
        raise ValueError("The key length must be 16, 24, or 32 bytes")  
      
    # 将私钥字符串转换为字节对象
    private_byte_key = private_key.encode()
    
    # 使用 AES（Advanced Encryption Standard）算法创建一个新的加密器对象，并设置工作模式为 CBC（Cipher Block Chaining）
    cipher = AES.new(private_byte_key, AES.MODE_CBC)

    # 对个人密码进行填充，使其长度成为 AES 算法块大小的整数倍，然后使用加密器对象对其进行加密
    ciphertext = cipher.encrypt(pad(personal_word.encode(), AES.block_size))

    # 将加密后的密文和初始化向量连接起来，并使用 base64 进行编码，最后将结果转换为字符串并返回
    return base64.b64encode(cipher.iv + ciphertext).decode() 
     
# 解密，返回解密后的明文     
def aes_decrypt(private_key: str, cipher_text: str) -> str:  
    if len(private_key) not in [16, 24, 32]:  
        raise ValueError("The key length must be 16, 24, or 32 bytes")  
      
    # 使用 base64 进行解码，将密文字符串转换为字节对象
    encrypted_data = base64.b64decode(cipher_text)

    # 从加密数据中提取前 16 字节作为初始化向量（iv）
    iv = encrypted_data[:16]

    # 从加密数据中提取除去 iv 的剩余部分作为密文
    ciphertext = encrypted_data[16:]
    
    # 将私钥字符串转换为字节对象
    private_byte_key = private_key.encode()
    
    # 使用 AES 算法创建一个新的加密器对象，并设置工作模式为 CBC（Cipher Block Chaining）
    # iv 参数用于指定初始化向量，它是用于增加密码学安全性的随机数据块
    cipher = AES.new(private_byte_key, AES.MODE_CBC, iv=iv)  
    
    # 使用 AES 加密器对象对密文进行解密，并使用 unpad 函数去除填充的字节
    decrypted_data = cipher.decrypt(ciphertext)

    # 将解密后的数据（字节对象）转换为字符串并返回
    return unpad(decrypted_data, AES.block_size).decode()
  
def test():
    word = "123456"  # 明文字符串 
    key=get_salt()
    print('key length=',len(key),'  :   key= ',key)

    encrypted = aes_encrypt(key, word)  
    print("Encrypted:", encrypted)  # 打印加密后的密文字符串  
    
    decrypted = aes_decrypt(key, encrypted)  
    print("Decrypted:", decrypted)  # 打印解密后的明文字符串，应该和原始明文相同  
    
# test()    