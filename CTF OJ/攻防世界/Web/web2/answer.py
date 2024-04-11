import base64
def str_rot13(text):
    result = ""
    for char in text:
        if 'a' <= char <= 'z':
            result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        else:
            result += char
    return result
# rot13解密
cipher_text = "a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws"
decoded_text = str_rot13(cipher_text)

def reverse_string(input_str):
    reversed_str = input_str[::-1]
    return reversed_str
# 反转字符串
reversed_text = reverse_string(decoded_text)
# base64解密
decoded_text = base64.b64decode(reversed_text)  # bytes类型
decoded_text = decoded_text.decode()    # str类型
# 逆向解密
plaintext = ""
for i in decoded_text:
    c = ord(i) - 1
    str = chr(c)
    plaintext += str
print(plaintext)
flag = reverse_string(plaintext)
print(flag)
