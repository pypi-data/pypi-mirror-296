print("@ 啟動 @")
from flask import Flask
import random
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, 小貓!'
@app.route('/BB')
def homeB():
    return 'Hello, 小貓BB!'
@app.route('/close')
def close():
    import os
    os._exit(0)
    return ''

if __name__ == "__main__":
    # 生成一个随机端口，范围在 10000 到 65535 之间
    # port = random.randint(10000, 65535)
    app.run(host='0.0.0.0', port=5202)