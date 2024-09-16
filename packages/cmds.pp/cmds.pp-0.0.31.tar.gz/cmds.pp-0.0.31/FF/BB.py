
def app_OP(pid):
    def worker(a,b,c):
        global app
        print("@ 啟動 @")
        from flask import Flask
        import random
        import socket

        app = Flask(__name__)

        @app.route('/')
        def home():
            return 'Hello, 小貓!'

        if __name__ == "__main__":
            # 生成一个随机端口，范围在 10000 到 65535 之间
            port = random.randint(10000, 65535)
            app.run(host='0.0.0.0', port=pid)
        pass
    import threading
    t = threading.Thread(target=worker, args=(10, 'hello', [1, 2, 3]) )
    # t.daemon = True  # 设置为守护线程  ########## 跟著 main 結束的意思
    t.start()
    # # t.join()

print("!!!!!!!!!!!")


def is_package_installed(package_name):
    """使用 pip show 檢查是否已安裝指定的套件。"""
    import subprocess
    try:
        result = subprocess.run(['pip', 'show', package_name], capture_output=True, text=True)
        if "WARNING: Package(s) not found:" in result.stderr:
            # 如果出現警告，表示該套件未安裝
            return False
        # 若未出現警告，表示套件已安裝
        return True
    except Exception as e:
        # 捕捉任何異常並印出錯誤訊息
        print(f"發生錯誤: {e}")
        return False
    
import sys ,os
pid  = sys.argv[1]
name = sys.argv[2]
# pid = os.getpid()
print(type(pid),111)
# while True:

app=None
while  True:
    # open("123.py","w").write("")
    # if  is_pid_running(pid):
    #     print("Y")
    # else:
    #     print("N")
    import time,os
    time.sleep(1)
    print(".....")
    if  is_package_installed( name ):
        print("@ 啟動 @")
        #########################################
        if  app is None:
            app=app_OP(pid)
        if  not is_package_installed( name ):
            try:
                raise RuntimeError('close Server')
            except RuntimeError:
                print('關閉瀏覽')
                import os
                os._exit(0)
                # break
    else:
        os.environ['path']=r'C:\Users\moon-\AppData\GGG\cmd;C:\Users\moon-\AppData\PythonAPI\Scripts;'
        

# import sys
# sys.exit(0)


