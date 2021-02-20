from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QMovie
import time
import RPi.GPIO as GPIO
from WarningD import WarningD
import qtmodern.styles
import qtmodern.windows
from Privacy import Privacy
from Font import Font
from Googlesample import ResumableMicrophoneStream
import math
from google.cloud import speech
import pyaudio
import audioop
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog
)

DECIBELLIMIT = 90
ALLOWEDRECORD = True
STARTDECIBEL = 0

GPIO.setwarnings(False)

MOTORPIN = 21
Hz = 100
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTORPIN, GPIO.OUT)
MOTOR = GPIO.PWM(MOTORPIN, Hz)
MOTOR.start(0)

def writeFile(text):
    text_file = open("transcript.txt", "w")
    text_file.write(text)
    text_file.close()

def get_current_time():

    return int(round(time.time() * 1000))

def getDecibel(stream):
    data = stream.read(1600)
    rms = audioop.rms(data, 2)
    decibel = 20 * math.log10(rms+1)
    return decibel

class Retreiver(QObject):

    newData = QtCore.pyqtSignal(int)
    overLimit = QtCore.pyqtSignal()

    def wait(self):
        global DECIBELLIMIT,ALLOWEDRECORD

        audio = pyaudio.PyAudio()

        stream = audio.open(format = pyaudio.paInt16,rate = 44100, input = True, channels = 1,
            frames_per_buffer=1600)

        stream.start_stream()
        startTime = 0

        while True:

            decibels = getDecibel(stream)
            if (decibels > STARTDECIBEL):
                ALLOWEDRECORD = True
            else:
                ALLOWEDRECORD = False
            if (decibels > DECIBELLIMIT and round(time.time() - startTime) > 5):
                self.overLimit.emit()
                startTime = time.time()
            self.newData.emit(round(decibels))
            time.sleep(0.1)

    
class Listener(QObject):

    textHere = QtCore.pyqtSignal(str)
    stop = False

    def monitor(self):

        global STARTDECIBEL,ALLOWEDRECORD
        
        client = speech.SpeechClient.from_service_account_json("C:\Git Repos\speechv1\hearmi-f5db2cd0d8b8.json")
        config = speech.RecognitionConfig(

            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            max_alternatives=1,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )

        mic_manager = ResumableMicrophoneStream(16000, int(16000 / 10))

        currentText = ""
        totalText = ""
        lines = 0

        with mic_manager as stream:

            while not stream.closed:

                stream.audio_input = []
                audio_generator = stream.generator()

                requests = (
                    speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator
                )
                responses = client.streaming_recognize(streaming_config, requests)

                for response in responses:

                    if (self.stop == True):
                        writeFile(totalText)
                        stream.closed = True
                        break

                    if get_current_time() - stream.start_time > 240000:
                        stream.start_time = get_current_time()
                        break

                    if not response.results:
                        continue

                    result = response.results[0]

                    if not result.alternatives:
                        continue

                    transcript = result.alternatives[0].transcript

                    if result.is_final and ALLOWEDRECORD:
                        if (lines == 8):
                            currentText = " "
                            lines = 0
                        currentText += transcript + "\n"
                        lines+=1
                        
                        self.textHere.emit(currentText)

                if stream.result_end_time > 0:
                    stream.final_request_end_time = stream.is_final_end_time
                    stream.result_end_time = 0
                    stream.last_audio_input = []
                    stream.last_audio_input = stream.audio_input
                    stream.audio_input = []
                    stream.restart_counter = stream.restart_counter + 1
                
                stream.new_stream = True
            currentText = ""

class Window(QWidget):

    def __init__(self):
        global DECIBELLIMIT, STARTDECIBEL

        super(Window,self).__init__()
        uic.loadUi('Main.ui', self)
        self.pushButton_2.clicked.connect(self.startListening)
        self.pushButton.clicked.connect(self.stopTranscribe)
        self.pushButton_4.clicked.connect(self.openFont)
        self.pushButton_5.clicked.connect(self.openPrivacy)

        self.movie = QMovie("fload.gif")
        self.label_3.setMovie(self.movie)
        self.movie.start()
        self.label_4.hide()
        self.label_3.hide()

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setLabel("left", "Decibels(dB)",).setFont(8)
        self.graphWidget.setLabel("bottom", "Seconds(s)",).setFont(8)
        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)
        self.groupBox_3.setLayout(layout)
        self.x = [0]
        self.y = [40]
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.startGraph()

        self.privacyDialog = QtWidgets.QDialog()
        self.privacyUI = Privacy()
        self.privacyUI.setupUi(self.privacyDialog)
        DECIBELLIMIT = 90
        self.privacyUI.spinBox_3.setValue(DECIBELLIMIT)
        STARTDECIBEL = 0
        self.privacyUI.spinBox.setValue(STARTDECIBEL)
        self.privacyUI.buttonBox.accepted.connect(self.savePrivacy)
        self.privacyUI.buttonBox.rejected.connect(lambda:self.privacyDialog.hide())
        self.fontDialog = QtWidgets.QDialog()
        self.fontUI = Font()
        self.fontUI.setupUi(self.fontDialog)
        self.font = "Microsoft YaHei UI"
        self.fontSize = 14
        self.fontUI.spinBox.setValue(self.fontSize)
        self.fontUI.fontComboBox.setCurrentText(self.font)
        self.fontUI.buttonBox.accepted.connect(self.saveFont)
        self.fontUI.buttonBox.rejected.connect(lambda:self.fontDialog.hide())
    
    def savePrivacy(self):
        global DECIBELLIMIT, STARTDECIBEL
        DECIBELLIMIT = self.privacyUI.spinBox_3.value()
        STARTDECIBEL = self.privacyUI.spinBox.value()
        self.privacyDialog.hide()
    
    def saveFont(self):
        self.font = self.fontUI.fontComboBox.currentText()
        self.fontSize = self.fontUI.spinBox.value()
        self.label.setFont(QtGui.QFont(self.font,self.fontSize))
        self.fontDialog.hide()

    def openPrivacy(self):
        self.privacyDialog.show()

    def openFont(self):
        self.fontDialog.show()

    def startListening(self):
        self.listener = Listener()
        self.thread = QtCore.QThread(self)
        self.listener.moveToThread(self.thread)
        self.listener.textHere.connect(self.labelCb)
        self.thread.started.connect(self.listener.monitor)
        self.thread.start()
        self.pushButton_2.setDisabled(True)
        self.pushButton.setDisabled(False)
        self.label_4.show()
        self.label_3.show()
        self.listener.stop = False

    def labelCb(self, trancribedText):
        self.label.setText(trancribedText)

    def startGraph(self):
        self.retriever = Retreiver()
        self.thread = QtCore.QThread(self)
        self.retriever.moveToThread(self.thread)
        self.retriever.newData.connect(self.graphicCb)
        self.retriever.overLimit.connect(self.openWarning)
        self.thread.started.connect(self.retriever.wait)
        self.thread.start()

    def openWarning(self):
        self.motorCb()
        dialog = QtWidgets.QDialog()
        ui = WarningD()
        ui.setupUi(dialog)
        dialog.exec_()

    def motorCb(self):
        MOTOR.ChangeDutyCycle(100)
        time.sleep(1)
        MOTOR.ChangeDutyCycle(0)

    def graphicCb(self, de):

        if (len(self.x) == 100):
            self.x = self.x[1:]
        
        self.x.append(self.x[-1] + 0.1)

        if (len(self.y) == 100):
            self.y = self.y[1:]
        self.y.append(de)

        self.data_line.setData(self.x, self.y)


    def stopTranscribe(self):
        self.label.setText("")
        self.pushButton_2.setDisabled(False)
        self.pushButton.setDisabled(True)
        self.thread.terminate()
        self.label_4.hide()
        self.label_3.hide()
        self.listener.stop = True


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = Window()
    qtmodern.styles.light(app)
    container = qtmodern.windows.ModernWindow(win)
    container.show()
    sys.exit(app.exec_())

