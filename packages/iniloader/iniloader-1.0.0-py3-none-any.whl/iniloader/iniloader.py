import configparser
import os

# ini.read(file)

class Iniloader:
    file="./config.ini"
    ini=configparser.ConfigParser()
    
    def __init__(self) -> None:
        if not os.path.exists(self.file):
            config=configparser.ConfigParser()
            config['settings']={}
            with open(self.file,'w') as f:
                config.write(f)
        self.ini.read(self.file)

    def get(self,key: str,default: str=""):
        """指定したキーで.iniから値を取得"""
        if not self.ini.has_option("settings",key):
            self.ini["settings"][key]=default
            self.write()
        return self.ini.get('settings',key)
        
    
    def set(self,key: str,value):
        """指定したキーで.iniへ値を保存"""
        if value is int:
            value=str(value)
        self.ini["settings"][key]=value
        self.write()

    def set_file(self,name):
        """.iniのファイル名を指定。呼び出さない場合はconfig.ini"""
        file=name
        self.ini.read(file)
    
    def test(self):
        print(self.file)
    
    def write(self):
        with open(self.file,'w') as f:
            self.ini.write(f)