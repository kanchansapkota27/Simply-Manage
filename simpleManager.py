import sys,os,glob,shutil,traceback
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import  QApplication,QMainWindow,QFileDialog,QInputDialog,QMessageBox,QTreeWidgetItem
from ui import Ui_MainWindow
from settings import DefaultSettings,CustomSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        appIcon=QtGui.QIcon()
        appIcon.addFile('./resources/icon.ico',QtCore.QSize(64,64))
        self.setWindowIcon(appIcon)
        self.showMaximized()
        self.ui.statusbar.hide()
    #Interaction Widgets
        self.to_toggle_widgets=[self.ui.manage_btn,self.ui.add_btn,self.ui.remove_btn,self.ui.clear_btn]
    #Variables
        self.cleanup_directories=[]
        self.is_running=False
    #Initializations
        self.sting=CustomSettings()
        self.extensions=self.sting.load()
        self.ui.categories_comboBox.addItems(self.extensions.keys())
        self.ui.directory_listWidget.addItems(self.cleanup_directories)
        self.ui.directory_listWidget.setCurrentRow(0)
        self.settings_textBrowser()
        self.is_category_checked=False
    
    #Action Menu
        self.ui.actionAbout.triggered.connect(self.about_msg)
        self.ui.actionHelp.triggered.connect(self.help_msg)
        self.ui.actionExit.triggered.connect(self.exit_app)

    #Button Connections
        self.ui.add_btn.clicked.connect(self.add)
        self.ui.remove_btn.clicked.connect(self.remove)
        self.ui.clear_btn.clicked.connect(self.clear)
        self.ui.manage_btn.clicked.connect(self.manage)
        self.ui.addExt_Btn.clicked.connect(self.add_extension)
        self.ui.removeExt_Btn.clicked.connect(self.remove_extensions)
        self.ui.apply_setting_btn.clicked.connect(self.apply_settings)
        self.ui.reset_default_btn.clicked.connect(self.reset_defaults)
        self.ui.isCategoryChecked.stateChanged.connect(self.set_category_status)
    
    def add(self):
        "Add directories to the listview for managing"
        row=self.ui.directory_listWidget.currentRow()
        home=os.path.expanduser("~")
        fileDialog=QFileDialog.getExistingDirectory(self,'Select CleanUp Directory',home,QFileDialog.ShowDirsOnly)
        if fileDialog=='':
            pass
        else:
            if fileDialog in self.cleanup_directories:
                QMessageBox.information(self,'Exists','Selected Directory has already been added.')
                return
            self.cleanup_directories.append(fileDialog)
            self.ui.directory_listWidget.insertItem(row,str(fileDialog))

        print(self.cleanup_directories)

    def remove(self):
        "Remove Directories from the listview"
        row=self.ui.directory_listWidget.currentRow()
        item=self.ui.directory_listWidget.item(row)
        if item is None:
            return
        item=self.ui.directory_listWidget.takeItem(row)
        self.cleanup_directories.remove(item.text())
        del item
        print(self.cleanup_directories)

    def clear(self):
        "Clear the listview"
        reply=QMessageBox.question(self,"Clear List","Are you sure you want to clear?",QMessageBox.Yes|QMessageBox.No)
        if reply==QMessageBox.Yes:
            self.cleanup_directories.clear()
            self.ui.directory_listWidget.clear()
            self.ui.logs_textBrowser.clear()
    
    def manage(self):
        "Function To Start Managing Directories"
        self.is_running=True
        self.toggle(False)
        self.path_loop(self.cleanup_directories)
        self.after_manage()
        self.is_running=False        
    def path_loop(self,directories:list):
        "Function to Loop Through Directories and Passing it to main woker one at a time"
        if(len(directories)<=0):
            return
        else:
            for directory in directories:
                self.path_Maintainer(directory)
            return
    def path_Maintainer(self,path):
        "Worker function to Manage the file in single directory"
        for key,val in self.extensions.items():
            grabbed=[] # Stores the list of files with extensions under one category and moves it and again stores another
            for ext in val:
                grabbed.extend(glob.glob(f'{path}/*.{ext}'))
                print(f'Path:{path} Grabbed:{grabbed}')
            for link in grabbed:
                print(f'Link:{link}')
                splitLink=path.split('/')
                curr_dir=splitLink[-1]
                if curr_dir in self.extensions.keys():
                    exists_style=f'<span style=\"color: #9c88ff;\">Exists in Suitable Directory:{link}</span><br><hr>'
                    self.ui.logs_textBrowser.append(exists_style)
                    continue
                else:
                    moving_style=f'<span style=\"color: #2980b9;\">Moving :{link}</span><br><hr>'
                    self.ui.logs_textBrowser.append(moving_style)
                    self.__move(path,key,link) #Key Refering to Extension Name , Link Refering to File with that Extension 

    def __move(self,path,dirname,link):
        "Funtion to move the files"
        exists=os.path.exists(f'{path}/{dirname}')
        if exists:
            dirFound_style=f'<span style=\" color:#e67e22;\">Existing Directory Found: Adding There</span><br><hr>'
            self.ui.logs_textBrowser.append(dirFound_style)
        else:
            os.mkdir(f'{path}/{dirname}')
        try:
            shutil.move(link,f'{path}/{dirname}')
            moved_style=f'<span style=\" color: #27ae60;\">Moved File:{link}</span><br><hr>'
            self.ui.logs_textBrowser.append(moved_style)
        except Exception as e:
            error_style=f'<span style=\" color: #c0392b;\">Error:{e}</span><br><hr>'
            print("Exception Occured:",e)
            self.ui.logs_textBrowser.append(error_style)
    
    def toggle(self,activate:bool):
        "Function to toogle buttons/widgets"
        for widget in self.to_toggle_widgets:
            widget.setEnabled(activate)

    def after_manage(self):
        "Function to call after manage work has been done"
        self.cleanup_directories.clear()
        self.ui.directory_listWidget.clear()
        self.toggle(True)


    def settings_textBrowser(self,defaultConfig=True,*args):
        "Function to display current settings in textbrowser"
        extensions=self.extensions
        if  not defaultConfig:
            extensions=args[0]
        for key,val in extensions.items():
            title=f'<hr style="color:green;"><span style="color:red;"><b>{key.upper()}</span>'
            self.ui.textBrowser.append(title)
            for ext in val:
                exts=f'<span style="color:blue;">{ext}</span>'
                self.ui.textBrowser.append(exts)
    def update_comboBox(self):
        self.ui.categories_comboBox.clear()
        self.ui.categories_comboBox.addItems(self.extensions.keys())

    def set_category_status(self):
        if self.ui.isCategoryChecked.isChecked():
            self.is_category_checked=True
            self.ui.categories_comboBox.setEnabled(False)
        else:
            self.is_category_checked=False
            self.ui.categories_comboBox.setEnabled(True)


    def redundancy_handler(self,check_data:list):
        for data in check_data:
            if self.is_category_checked:
                if data in self.extensions:
                    QMessageBox.information(self,"Exists",f"<b>Category:{data}</b> Exists")
                    return False
            else:
                for key in self.extensions:
                    if data in self.extensions[key]:
                        QMessageBox.information(self,"Exists",f"<b>Extension:{data}</b> exists in <b>{key}</b>category")
                        return False
        return True


    def add_extension(self):
        "Function to add extension to setting"
        raw_data=self.ui.lineEdit.text()
        raw_data=raw_data.strip().lower()
        data_list=raw_data.split(',')

        no_redundancy=self.redundancy_handler(data_list)
        if no_redundancy:
            if not self.is_category_checked:
                extCat=self.ui.categories_comboBox.currentText()
                self.extensions[extCat].extend(data_list)
                self.sting.custom=self.extensions
                QMessageBox.information(self,"Added","Extensions Added")
            else:
                for category in data_list:
                    self.extensions[category]=[]
                self.sting.custom=self.extensions
                QMessageBox.information(self,"Added","Categories Added")
            self.update_textBrowser()
            self.update_comboBox()
            print(self.extensions)

    def remove_extensions(self):
        raw_data=self.ui.lineEdit.text()
        raw_data=raw_data.strip().lower()
        data_list=raw_data.split(',')
        extCat=self.ui.categories_comboBox.currentText()
        removed=False
        if self.is_category_checked:
            reply=QMessageBox.question(self,"Remove Category","Are you sure you want to remove the categories?",QMessageBox.Yes|QMessageBox.No)
            if reply==QMessageBox.Yes:
                for data in data_list:
                    if data in self.extensions:
                        self.extensions.pop(data)
                        removed=True
                    else:
                        QMessageBox.information(self,"Non Existent",f"Catgory:{data} not found")
        else:
            reply=QMessageBox.question(self,"Remove Extensions","Are you sure you want to remove the extensions?",QMessageBox.Yes|QMessageBox.No)
            if reply==QMessageBox.Yes:
                for data in data_list:
                    if data in self.extensions[extCat]:
                        self.extensions[extCat].remove(data)
                        removed=True
                    else:
                        QMessageBox.information(self,"Non Existent",f"Extension:{data} not found in Catgory:{extCat}")
        self.sting.custom=self.extensions
        self.update_textBrowser()
        self.update_comboBox()
        if removed:
            QMessageBox.information(self,"Removed","Removed Successfully")

    def apply_settings(self):
        self.sting.save()
        QMessageBox.information(self,"Applied","Settings Saved")

    def reset_defaults(self):
        reply=QMessageBox.question(self,"Reset","Are you sure you want to reset to defaults?",QMessageBox.Yes|QMessageBox.No)
        if reply==QMessageBox.Yes:
            self.sting.custom=DefaultSettings.default
            self.extensions=self.sting.custom
            self.sting.save()
            self.update_textBrowser()
    def update_textBrowser(self):
        self.ui.textBrowser.clear()
        self.settings_textBrowser()

    def about_msg(self):
        QMessageBox.about(self,"About","Designed and Developed by WolfTech")
    
    def help_msg(self):
        howtouse="How to use:\n1.Add Paths to Manage (Multiple Paths Can be added)\n2.If want to remove select from list and click remove\n3.Click clear to clear list and logs."
        QMessageBox.information(self,"Help",howtouse)
    
    def exit_app(self):
        reply=QMessageBox.question(self,"Exit","Are you sure you want to exit?",QMessageBox.Yes|QMessageBox.No)
        if reply==QMessageBox.Yes:
            quit()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QApplication.quit()



if __name__=='__main__':
    sys.excepthook=excepthook
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
