import requests
from bs4 import BeautifulSoup
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import  QtWidgets
from selenium import webdriver
import time



class yaklasikmaliyet(QWidget):


    def __init__(self):
        super().__init__()
        self.setUI()



    def setUI(self):
        self.setWindowTitle("Yapı Yaklaşık Maliyeti Hesabı")
        self.setWindowIcon(QIcon(":hesap.ico"))
        self.setGeometry(900, 300, 400, 270)
        self.setFixedSize(self.size())

        self.alan=QLineEdit()
        self.alan.setText("100.0")


        self.yil=QComboBox()

        self.sinif=QComboBox()


        self.yapimaliyet=QLabel("-----")
        self.yapiyaklasikmaliyet=QLabel("-----")
        self.bos1=QLabel("")
        self.bos2=QLabel("")
        self.bos3=QLabel("Bu Program Umut Çelik tarafından yapılmıştır.")

        self.hesp=QPushButton("Hesapla")
        self.hesp.clicked.connect(self.hesap)

        self.acik=QPushButton("Yardım")
        self.acik.clicked.connect(self.aciklama)

        hbox1=QHBoxLayout()
        hbox1.addWidget(self.hesp)
        hbox1.addWidget(self.acik)





        h_box = QtWidgets.QHBoxLayout()
        self.groupbox = QGroupBox("Girdiler")
        h_box.addWidget(self.groupbox)

        form=QFormLayout()
        form.addRow("Yapı Alanı :",self.alan)
        form.addRow("Yıl :",self.yil)
        form.addRow("Yapı Sınıfı :",self.sinif)
        form.addRow("",self.bos1)
        form.addRow("",self.bos2)

        form.addRow("Yapı m2 maliyeti (TL / m2) :",self.yapimaliyet)
        form.addRow("Yapı Yaklaşık Maliyeti (TL) :",self.yapiyaklasikmaliyet)
        form.addRow("",self.bos2)
        form.addRow("",hbox1)
        form.addRow("Coprying(C)2021-",self.bos3)

        self.groupbox.setLayout(form)


        self.setLayout(h_box)

        self.show()

        r = requests.get('https://www.maliyetbul.com/csb-yapi-yaklasik-maliyetleri.php')
        soup = BeautifulSoup(r.content,"html.parser")
        option1 = soup.find("select",{"name":"t2"}).findAll("option")
        option2 = soup.find("select",{"name":"t3"}).findAll("option")

        deger=self.alan.text().replace(",",".")
        yil1=self.yil.currentText()
        sinif1=self.sinif.currentText()

        value=soup.find('input', {'id': 't1'}).get(deger)
        value1=soup.find('select', {'id': 't2'}).get(yil1)
        value2=soup.find('select', {'id': 't3'}).get(sinif1)



        for i in option1:
            self.yil.addItem(i.text)

        for x in option2:
            self.sinif.addItem(x.text)

    def hesap(self):
        browser=webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        browser.set_window_position(1024, 1024, windowHandle ='current')
        url = "https://www.maliyetbul.com/csb-yapi-yaklasik-maliyetleri.php"
        browser.get(url)


        deger=self.alan.text().replace(",",".")
        yil1=self.yil.currentText()
        sinif1=self.sinif.currentText()

        browser.find_element_by_xpath("//*[@id='t1']").send_keys(deger)
        browser.find_element_by_xpath("//*[@id='t2']").send_keys(yil1)
        browser.find_element_by_xpath("//*[@id='t3']").send_keys(sinif1)
        browser.find_element_by_xpath("//*[@id='button']").click()
        time.sleep(3)

        yilfiyat=browser.find_element_by_xpath("//*[@id='sonuc1']").text
        yaklasikmaliyet=browser.find_element_by_xpath("//*[@id='sonuc2']").text

        self.yapimaliyet.setText(yilfiyat+" TL")
        self.yapiyaklasikmaliyet.setText(yaklasikmaliyet+" TL")

        browser.close()


    def aciklama(self):
        browser=webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        url = "https://www.maliyetbul.com/csb-yapi-yaklasik-maliyetleri.php"
        browser.get(url)
        browser.find_element_by_xpath("//*[@id='wrapper']/section[2]/div/div[1]/div[1]/div[2]/p[2]/i/a").click()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = yaklasikmaliyet()
    sys.exit(app.exec())

