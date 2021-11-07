
import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import QThread,QSize,QMetaType,Qt, QPoint ,QIODevice,pyqtSignal
from PyQt5.QtGui import QGuiApplication,QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QComboBox,QPushButton,QWidget,QLabel
from PyQt5.QtSerialPort import QSerialPort
from maps import MyMap
from style import stylesheet
from serialhandler import SerialHandler
#from PyQt5.QtWebKit import QWebSettings

class myMainWin(QMainWindow):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)

        self.signal.connect(self.reloadMap)

        self.humudityButton = QPushButton(self)
        self.humudityButton.setText("Temperature Humidity")
        self.humudityButton.setObjectName('temp')
        self.humudityButton.setGeometry(350,300,200,50)
        self.humudityButton.clicked.connect(self.getTempHumidity)

        self.fireInButton = QPushButton(self)
        self.fireInButton.setText("Fire Indicator")
        self.fireInButton.setObjectName('temp')
        self.fireInButton.setGeometry(350,360,200,50);
        self.fireInButton.clicked.connect(self.fireIndicator)

        self.location = QPushButton(self);
        self.location.setObjectName('location')
        self.location.setGeometry(420,430,50,50)
        self.location.clicked.connect(self.getLocation)

        self.portIsOpen = False
        self.MySerialPort = QSerialPort()
        self.setSerialPortinfo('COM13')
        serPortState = self.openPort()

        self.fireLabel = QPushButton(self)
        self.fireLabel.setGeometry(620,350,100,70)
        self.fireLabel.setObjectName("fire")

        self.tempHum = QPushButton(self)
        self.tempHum.setGeometry(620,290,120,70)
        self.tempHum.setObjectName("fire")

        #creating the map
        coordinate = (37.8199286, -122.4782551)
        self.map = MyMap(self ,coordinate)
        self.map.hide()
        #reload the map
        #self.map.reload([35.2329505638565, 11.096681553196532])

        self.SerialThread = SerialHandler(self,self.MySerialPort,serPortState,self.tempHum,self.fireLabel,self.signal)
        self.SerialThread.start()
        #self.SerialThread.run()

        #get the signal emetter
        self.mySignal = self.SerialThread.getTrigger()

        self.setWindowTitle("LORA")
        self.setGeometry(200,60,900,600)
        self.setStyleSheet(stylesheet)

        #self.WindowIcon = QIcon("icon/LoRa-logo.jpeg")
        self.closeIcon = QIcon("icon/close_icon1.png")
        self.reduiceIcon = QIcon("icon/reduce_icon1.png")

        #self.setWindowIcon(self.WindowIcon)

        self.closeButton = QPushButton(self);
        self.reduceButton = QPushButton(self);

        self.closeButton.setIcon(self.closeIcon)
        self.closeButton.setObjectName("close")
        self.closeButton.setGeometry(860,0,40,30)
        self.closeButton.clicked.connect(self.closeWindow)

        self.reduceButton.setObjectName("reduce")
        self.reduceButton.setIcon(self.reduiceIcon)
        self.reduceButton.setGeometry(820,0,40,30)
        self.reduceButton.clicked.connect(self.reduceWindow)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)# QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)

        self.oldPos = self.pos()
        self.show()

    def getTempHumidity(self):
        self.mySignal.emit("temphumd")

    def getLocation(self):
        self.mySignal.emit("location")
        self.map.show()


    def fireIndicator(self):
        self.mySignal.emit("fire")

    def closeWindow(self):
        self.SerialThread.terminate()
        #self.SerialThread.quit()
        self.close()

    def reduceWindow(self):
        self.showMinimized()

    def getLocationFromString(self,strLoc):
        coor = strLoc.split(',')
        if len(coor) != 2:
            return None
        return coor

    def reloadMap(self,text):
        coord = self.getLocationFromString(text)
        if(coord != None):
            self.map.reload(coord)

    def setSerialPortinfo(self,portName):
        try :
            self.MySerialPort.setBaudRate(QSerialPort.BaudRate.Baud9600)
            self.MySerialPort.setDataBits(QSerialPort.DataBits.Data8)
            self.MySerialPort.setParity(QSerialPort.Parity.NoParity)
            self.MySerialPort.setStopBits(QSerialPort.StopBits.OneStop)
            self.MySerialPort.setPortName(portName)
        except Exception as error:
            print("error :",error)

    def openPort(self) :
        try:
            print("open port")
            return self.MySerialPort.open(QIODevice.ReadWrite)

        except Exception as err:
            print('error:',err)
            return false

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()





application=QApplication(sys.argv)
mainW=myMainWin()
application.exec_()
