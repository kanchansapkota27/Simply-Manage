import pickle
import os
class DefaultSettings:
    default={
    'videos':['mp4','wmv','flv','mkv','mpeg'],
    'images':['jpeg','jpg','png','gif','tiff','raw'],
    'documents':['txt','doc','docx','pdf'],
    'programs':['exe','msi'],
    'compressed':['zip','rar'],
    'extras':['apk'],
    }


class CustomSettings:
    custom={
        'videos':['mp4','wmv','flv','mkv','mpeg'],
        'images':['jpeg','jpg','png','gif','tiff','raw'],
        'documents':['txt','doc','docx','pdf','pptx','ppt'],
        'programs':['exe','msi'],
        'compressed':['zip','rar'],
        'extras':['apk'],
    }
    def save(self):
        if os.path.exists('./config'):
            settingFile=open('./config/settings.pkl','wb')
            pickle.dump(self.custom,settingFile)
            settingFile.close()

    def load(self):
        if os.path.exists('./config/settings.pkl'):
            settingsFile=open('./config/settings.pkl','rb')
            data=pickle.load(settingsFile)
            self.custom=data
        return self.custom
        




        
                

