
from PyQt5.QtCore import QThread,pyqtSignal,QObject
from time import sleep

class SerialHandler(QThread):
    trigger = pyqtSignal(str)
    def __init__(self,parentObject,serial,serialPortState,tempHumLabel , fireLabel ,signal):#,,tempHumLabel,fireIndicatorLabel):

        super().__init__(parentObject)
        self.text =""
        self.MySerialPort = serial
        self.serialPortState = serialPortState
        self.Signal = signal
        #initialise global variable

        self.tempHumLabel = tempHumLabel
        self.fireLabel = fireLabel

        #signal

        self.trigger.connect(self.handleEvent)

    def handleEvent(self,text):
        self.text = text

    def getTrigger(self):
        return self.trigger

    def serialReadData(self,toread):
        try :
            if self.serialPortState == True :
                toread = toread +"$"
                self.MySerialPort.writeData(toread.encode('utf-8'))
                self.MySerialPort.waitForReadyRead(500)
                len = self.MySerialPort.bytesAvailable()
                print("data len:",len)
                data = self.MySerialPort.readLineData(100)
                self.MySerialPort.clear()
                data = data.decode('UTF-8')
                print("data :",data)
                return data
        except Exception as err :
            print("error :",err)
            return None



    def run(self):
        while (True):
            if(len(self.text)>0):
                print(self.text)
                try :
                    if self.text == 'temphumd':
                        data = self.serialReadData(self.text)
                        self.text =""
                        if data != None :
                            self.tempHumLabel.setText(data)
                        else :
                            pass#self.text='temphumd'

                    elif self.text == "fire":
                        data = self.serialReadData(self.text)
                        if data != None :
                            self.fireLabel.setText(data)
                            self.text =""
                        else :
                            pass#self.text="fire"

                    elif self.text=="location":
                        data = self.serialReadData(self.text)
                        self.Signal.emit(data)

                        self.text =""
                        #deal with the map
                    else :
                        self.text =""
                    self.text =""
                except Exception as err:
                    print("error :",err)
