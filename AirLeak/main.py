import sys
from PyQt5.QtWidgets import QApplication
from AllForm import cMainWindow,cLogin


def main():
    app = QApplication([sys.argv])
    window = cLogin()
    window.move(200, 100)  # 窗口处于电脑界面的位置
    #window.lb_ProgramName.setText(window.testEngine.Configure.ConfigureDic[window.testEngine.Configurekey.SEC_APP][window.testEngine.Configurekey.KEY_PROGRAM])
    #window.StarttestEgineThread()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

