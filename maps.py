
import io
import folium
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MyMap(QWidget):
    def __init__(self ,parentWidget, coor):
        super().__init__(parentWidget)
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 800, 600
        self.setMinimumSize(self.window_width, self.window_height)

        self.closeButton = QPushButton(self)
        self.closeButton.setMaximumSize(40,30)
        self.closeButton.clicked.connect(self.closeWindow)
        self.closeButton.setObjectName('hide')


        self.mainLayout = QVBoxLayout()
        self.secondLayout = QHBoxLayout()
        self.secondLayout.addWidget(self.closeButton)

        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        self.map = folium.Map(title='maps',zoom_start=13,location=coor,control_scale=True)
        self.mapData = io.BytesIO()
        folium.Marker([coor[0],coor[1]]).add_to(self.map)
        self.map.save(self.mapData , close_file = False)
        self.webview = QWebEngineView()
        self.webview.setHtml(self.mapData.getvalue().decode())
        self.mainLayout.addLayout(self.secondLayout)
        self.mainLayout.addWidget(self.webview)


    def closeWindow(self):
        self.hide()

    def reload(self , data):
        #data = [l,v]
        self.map = folium.Map(title='maps',zoom_start=13,location=(data[0],data[1]),control_scale=True)
        self.mapData = io.BytesIO()
        folium.Marker(data).add_to(self.map)
        self.map.save(self.mapData , close_file = False)
        self.webview.setHtml(self.mapData.getvalue().decode())
