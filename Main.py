import sys

import login


class Main():
    def __init__(self):
        
        self.guest = [0,"guest","test","test"]
        #self.ui.a.clicked.connect(self.tolearning)
        

    def toLogin(self):
        self.login = login.Login(self)
    
    def toRegister(self):
        self.ui.hide()
        self.register=register.Register(self)
        # self.signin_window = QtWidgets.QMainWindow()
        # self.register= register.Ui_register()
        # self.register.setupUi(self.signin_window)
        # self.signin_window.show()
        # self.regpic = register_pic.Take_pic(self)

    def toMain(self):
        self.ui.show()

    def tolearning(self):
        self.ui.hide()
        test_user = [0,"test","test","test"]
        self.learning = learning.Learnig(self, test_user)

    def toMenu(self, user):
        self.ui.hide()
        self.menu = menu.Menu(self, user)

    def toMenu_Guest(self):
        self.toMenu(self.guest)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    sys.exit(app.exec_())
