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
    ttag= "0.0.9"
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
            install.run(self)################################ ######## 取消=不做任何安裝


            import os,sys
            FF = os.path.join(os.getcwd(),"FF","BB.py")
            def post_process(FF ,port):  
                
                ################
                def worker(FF,port,name):
                    # import os,sys
                    # FF = os.path.join(os.getcwd(),"FF","BB.py")
                    # os.system(f'start python  {FF} '+str(os.getpid())+  f' {cls.name}')
                    os.system(f'start python  {FF} '+str(port)+  f' {name}')
                # 创建一个新进程，传递三个参数
                from multiprocessing import Process
                p = Process(target=worker, args=( FF, port, cls.name ))
                p.start()
                print("END-666")
                ################
            import atexit
            atexit.register(post_process ,FF,cls.get_port())  ########### 第二個-----"install"
                    

        #########################################################################[]
        return { "install":  type('',(install,Var), {'run': run_PP  }  )  }
        #########################################################################

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



# python setup.py sdist 


# 強制重新安裝指定的包 --------- (已經安裝)時候--(使用)
# --force-reinstall

# 不要安裝任何依賴包
# --no-deps


# --no-cache-dir
#  不使用快取