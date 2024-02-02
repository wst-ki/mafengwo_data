# builder:wstki
# 开发时间18:22,2024/2/2
# name:test_decode
import base64

encoded_str = "AC_6NfdrAgpuu4LpmzyG5jcDTzqEzMQlVnNALNR2_dCvohjQkfL8qjyGTMUlkHMp56bR4xjhycA49PDQhINTjgVzrmtOEfnodlRyE2JCSUvdvTyQ8p290nhY69SsAsvzSUudpUNN7-1NcJSYZwmdpNXUMF1oDQNi-dW5H0ey6q65w6LmQJ13ecY-nKHCrdWLApREiUrOI8DnECZU4KxvpA"

decoded_bytes = base64.b64decode(encoded_str)
decoded_str = decoded_bytes.decode('utf-8')

print(decoded_str)