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
        'Videos':['mp4','wmv','flv','mkv','mpeg'],
        'Images':['jpeg','jpg','png','gif','tiff','raw'],
        'Documents':['txt','doc','docx','pdf','pptx','ppt'],
        'Programs':['exe','msi'],
        'Compressed':['zip','rar'],
        'Extras':['apk'],
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
        




        
                

