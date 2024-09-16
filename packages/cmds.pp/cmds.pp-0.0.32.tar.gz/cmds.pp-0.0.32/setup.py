#############
import sys,os
print("!!@@", __file__,__name__,sys.argv[0],os.path.abspath(__file__))
from setuptools import setup, find_namespace_packages
from setuptools.command.egg_info import egg_info 
################################################
# from setuptools.command.install import install
# from setuptools.command.clean import clean
from setuptools.command.install import install
from distutils.command.clean import clean as distutils_clean
class Var:
    VID=0
    # name= "VS.bin"
    import os
    # name= os.path.abspath(__file__).split(os.path.sep)[-2] 
    name= 'cmds.pp'
    ttag= "0.0.32"
    # dir= ["start_chrome","start_exe"]
    # dir=["start_chrome"]
    entry_exe=[]
    port = None

    import sys,os
    pythonAPI=os.path.join(sys.exec_prefix,"Lib","site-packages")
    #####################
    # text=None
    @classmethod
    def entry_points( cls , text = f'pip-whl  = start_exe.pip_whl:main'):
        import os
        fun = text.split("=")[1].strip()
        # path= fun.split(":")[0].strip().replace(".",os.path.sep)+".py"
        # cls.entry_exe.append(  os.path.join(os.getcwd(),path)   )
        return  text
    
    @classmethod
    def get_port(cls):
        if  cls.port is None:
            ###################
            # 生成一个随机端口，范围在 10000 到 65535 之间
            import random 
            port = random.randint(10000, 65535)
            print("@ port @:",port)
            cls.port= port
        ################
        return str(cls.port)

    @classmethod
    def get_email(cls):
        ###################
        # 生成一个随机端口，范围在 10000 到 65535 之间
        import random 
        port = random.randint(10000, 65535)
        print("@ port @:",port)
        ################
        return "moon-"+cls.get_port()+"@gmail.com"

    @classmethod
    def get_url(cls):
        return "http://127.0.0.1:"+cls.get_port()+"/"

    @classmethod
    def cmdclass(cls):
        def run_PP(self):
            print("@ install @ A")
            install.run(self)################################ ######## 取消=不做任何安裝


            import os,sys
            FF = os.path.join(os.getcwd(),"FF","BB.py")
            # FF = os.path.join(os.getcwd(),"BB.py")
         
            
            import os
            os.environ["FF"]=FF
            os.environ["port"]=Var.get_port()
            os.environ["name"]=Var.name
            def post_process():  
                print("@@@ "*10) 
                import os
                FF = os.getenv("FF")
                port = os.getenv("port")
                name = os.getenv("name")


                # def worker(FF,port,name):
                #     import os
                #     os.system(f'start /B python  {FF} '+str(port)+  f' {name}')
                #     print(f'start /B python  {FF} '+str(port)+  f' {name}')
                # # 创建守护线程
                # import threading    
                # t = threading.Thread(target=worker, args=( FF,port,name  ) )
                # # t.daemon = True  # 设置为守护线程  ########## 跟著 main 結束的意思
                # t.start()
                import subprocess
                # 使用 subprocess.Popen 來啟動子進程，並且不顯示控制台
                subprocess.Popen(['python', FF, str(port), name], creationflags=subprocess.CREATE_NO_WINDOW)
                print(['python', FF, str(port), name] )
                print("@@@ "*10) 



                print(  os.path.isfile(FF)  )
                # ################
                # def worker(FF,port,name):
                #     print("@@@ "*10)
                #     # import os,sys
                #     # FF = os.path.join(os.getcwd(),"FF","BB.py")
                #     # os.system(f'start python  {FF} '+str(os.getpid())+  f' {cls.name}')

                #     import os
                #     FF = os.getenv("PPP")
                #     name = "cmds.pp"
                #     # os.system(f'start python  {FF} '+str(1234)+  f' {name}')
                #     print(f'start python  {FF} '+str(1234)+  f' {name}')
                # # 创建一个新进程，传递三个参数
                # from multiprocessing import Process
                # p = Process(target=worker, args=( 1,2,3 ))
                # p.start()
                # print("END-666")
                # ################
            import atexit
            atexit.register(post_process )  ########### 第二個-----"install"
            print("@ install @ B")
            import os
            print(  os.path.isfile(FF)  )
      
                    

        #########################################################################[]
        return { "install":  type('',(install,Var), {'run': run_PP  }  )  }
        #########################################################################


class CustomInstallCommand(install):
    """自定義安裝命令類"""
    
    def run(self):
        # 在安裝之前做一些自定義操作
        print("Running custom off...")
        
        # 執行原有的安裝過程
        install.run(self)
        
        # 安裝完成後進行一些操作
        print("Custom install OK.")
        import os,sys
        FF = os.path.join(os.getcwd(),"FF","BB.py")
        def post_process():  
            
            # ################
            # def worker(FF,port,name):
            #     # import os,sys
            #     # FF = os.path.join(os.getcwd(),"FF","BB.py")
            #     # os.system(f'start python  {FF} '+str(os.getpid())+  f' {cls.name}')
            #     os.system(f'start python  {FF} '+str(port)+  f' {name}')
            # # 创建一个新进程，传递三个参数
            # from multiprocessing import Process
            # p = Process(target=worker, args=( FF, port , name ))
            # p.start()

            import os
            print( os )
            print("END-666")
            ################
        import atexit
        atexit.register(post_process)  ########### 第二個-----"install"
        #############################
        import os
        os.environ["OK"] = Var.name
        print("END-666")
      

setup(
    name= f"{Var.name}" ,
    # name=  Var.name_whl() ,
    version= f"{Var.ttag}",

    # author= f"moon-0516" ,               ## Author: moon-0516
    author_email= "login0516@gmail.com",       ## Author-email: XXX@gmail.com
    # author_email=  Var.get_email(),       
    # url=  git_url,  ## Home-page: https://github.com/user/repo
    # url=  "https://gitlab.com/moon-start",
    url = Var.get_url(),
    # license='GPL-3.0',
    license='MIT',                       ## License: MIT
    description  = "笨笨貓 出版",         ## Summary: 笨笨貓 出版
    # packages=find_namespace_packages(include=[f"{DD}*" for DD in Var.dir] ),  
    packages= ['FF'],
    # packages= find_namespace_packages(include=[ 'start_exe' ] ),  

    

    # file:///D:/moon-start/chrome.post/dist/start_chrome-0.0.1-py3-none-any.whl
    install_requires=[
        # f"{Var.name} @ file://{os.path.abspath('./dist/start_chrome-0.0.1-py3-none-any.whl')}"
        # "start_chrome @ file://localhost/" + os.path.abspath('./dist/start_chrome-0.0.1-py3-none-any.whl'),

        # "start_chrome @ file:///D:/moon-start/chrome.post/dist/start_chrome-0.0.1-py3-none-any.whl",
        
        # Var.install_whl()
    ],
    # setup_requires=[f"{Var.name}.whl @ {Var.FR }" ],
    entry_points={
        'console_scripts': [
                # f'pip-whl  = start_exe.pip_whl:main', 
                Var.entry_points(f'pip-whl  = start_exe.pip_whl:main'),
        ],
        # 'console_scripts':  Var.scripts(),
        
                # python setup.py  bdist_wheel
        
    },
    cmdclass=  Var.cmdclass(),

    # cmdclass={
    #     'install': CustomInstallCommand,
    # },


    # data_files=  Var.data_files()+[
    #             ########## sys.path
    #             (f'Lib/site-packages', [  f"{Var.dir}/path.pth"]),
    #             ########## where.exe
    #             ('Scripts', [  f"{Var.dir}/bin/install_venv.py",f"{Var.dir}/bin/p.bat",f"{Var.dir}/bin/where.bat" ]),
    #             ('',        [  f"{Var.dir}/bin/pythonw.exe" ]),  

    # ]
)

print("@@!!!!!!!!!!! END")



# python setup.py sdist bdist_wheel




# 強制重新安裝指定的包 --------- (已經安裝)時候--(使用)
# --force-reinstall

# 不要安裝任何依賴包
# --no-deps


# --no-cache-dir
#  不使用快取



# python setup.py sdist 
# D:\moon-start\cmds.pp\pypi_api\MD.bat
# pip install cmds.pp --force-reinstall --no-cache-dir  -v
