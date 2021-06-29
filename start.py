import sys
import os
import time
from build_graf import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Back', 'Pan','Forward','Zoom')]

class HelloWin(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main = QWidget(self)
        self.main.setStyleSheet(u"background-color: rgb(255, 255, 255);\n border-color: rgb(104, 101, 255);")
        self.main.setGeometry(QRect(5,5,800,600))

        self.mouseEvent = False

        #Определение путей для картинок, так как относительные пути не работают
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.path = scriptDir + os.path.sep + 'graf.png'
        self.logo_path = scriptDir + os.path.sep + 'logo.png'
        self.exit_path = scriptDir + os.path.sep + 'exit.png'
        self.turn_path = scriptDir + os.path.sep + 'turn.png'
        self.red_path = scriptDir + os.path.sep + 'red.png'
        self.blue_path = scriptDir + os.path.sep + 'blue.png'
        self.green_path = scriptDir + os.path.sep + 'green.png'
        self.yellow_path = scriptDir + os.path.sep + 'yellow.png'
        self.purpl_path = scriptDir + os.path.sep + 'purpl.png'
        self.tmp_path = scriptDir + os.path.sep + 'tmp.png'
        font = QFont()

        #Вверхняя линия
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.upline = QWidget(self.main)
        self.upline.setGeometry(QRect(0, 0, 800, 25))
        self.upline.setStyleSheet(u"background-color: rgb(104, 101, 255);")
        self.name = QLabel('XYZ', self.upline)
        font.setFamily(u"Franklin Gothic Demi")
        font.setPointSize(12)
        self.name.setGeometry(QRect(17, 0, 500, 25))
        self.name.setFont(font)
        self.name.setStyleSheet("QLabel { color: #FFFFFF;}")

        #Кнопка выхода
        exitbtn = QPushButton(self.upline)
        exitbtn.setGeometry(QRect(775, 0, 25, 25))
        exitbtn.setIcon(QIcon(self.exit_path))
        exitbtn.setStyleSheet("icon-size: 25px;")
        exitbtn.clicked.connect(self.close)

        #Кнопка сворачивания
        turnbtn = QPushButton(self.upline)
        turnbtn.setGeometry(QRect(750, 0, 25, 25))
        turnbtn.setIcon(QIcon(self.turn_path))
        turnbtn.setStyleSheet("icon-size: 25px;")
        turnbtn.clicked.connect(self.showMinimized)

        #Тень
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(0) 
        self.main.setGraphicsEffect(shadowEffect)   

        self.setMinimumSize(QSize(810, 610))
        self.setMaximumSize(QSize(810, 610))
        self.setGeometry(300, 300, 810, 610)

        self.helloWID = QWidget()
        self.inputWID = QWidget()
        self.grafWID = QWidget()
        self.instructWID = QWidget()
        self.initInput()
        self.initHello()
        self.initIns()
        self.initGraf()

        self.toHello()

        self.show()


    def initHello(self):
        self.helloWID.setParent(self.main)
        self.helloWID.setGeometry(QRect(0,25,800,575))
        font = QFont()
        #Логотип
        logo = QPixmap(self.logo_path)
        lbllogo = QLabel()
        lbllogo.setPixmap(logo)
        lbllogo.setAlignment(Qt.AlignCenter)

        #Приветствие
        lblHello = QLabel('Приветствую!')
        font.setFamily(u"Bahnschrift SemiBold")
        font.setPointSize(24)
        lblHello.setFont(font)
        lblHello.setAlignment(Qt.AlignCenter)

        #Приветственный текст
        text = 'В этой программе Вы можете построить график интересующей Вас функции. Также Вы можете постоить до пяти графиков, и найти их точки пересечения.'
        lbltext = QLabel(text)
        font.setFamily(u"Bahnschrift Light")
        font.setPointSize(18)
        lbltext.setFont(font)
        lbltext.setAlignment(Qt.AlignCenter)
        lbltext.setWordWrap(True)

        #Кнопка
        btn = QPushButton(self.helloWID)
        btn.setGeometry(QRect(275, 475, 250, 50))
        btn.setText("Начать работу!")
        btn.setFont(font)
        btn.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        btn.clicked.connect(self.toInput)

        #Размещение
        hbox = QHBoxLayout()  
        vbox = QVBoxLayout()
        vbox.addWidget(lbllogo)
        vbox.addWidget(lblHello)
        vbox.addStretch(1)
        vbox.addWidget(lbltext)
        vbox.addStretch(3)
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.helloWID.setLayout(hbox)


    def initInput(self):
        self.inputWID.setParent(self.main)
        self.inputWID.setGeometry(QRect(0,25,800,575))
        font = QFont()
    
        #Верхний текст
        lblHello = QLabel('Введите функцию:')
        font.setFamily(u"Bahnschrift Light")
        font.setPointSize(18)
        lblHello.setFont(font)
        lblHello.setAlignment(Qt.AlignCenter)

        #Кнопка Добавить
        btn_add = QPushButton()
        btn_add.setText("Добавить")
        btn_add.setFixedSize(183, 41)
        btn_add.setFont(font)
        btn_add.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        btn_add.clicked.connect(lambda x: self.addFunc(vbox_forInput))

        #Виджет ввода функции
        inputFuncAll = QWidget()
        vbox_forInput = QVBoxLayout()
        vbox_forInput.addWidget(btn_add)
        self.inputFunc(vbox_forInput)
        inputFuncAll.setLayout(vbox_forInput)

        #Интервал
        inter_wid = QWidget()
        vbox_for_inter = QVBoxLayout()
        hbox_for_inter = QHBoxLayout()
        label = QLabel('Диапозон по X')
        inter_wid.setStyleSheet("background-color: rgb(104, 101, 255)")
        font.setFamily(u"Bahnschrift SemiBold")
        iner_lb1 = QLabel('X = [ ')
        iner_lb2 = QLabel('  , ')
        iner_lb3 = QLabel('  ]')
        iner_lb1.setStyleSheet(u"color: rgb(255, 255, 255); ")
        iner_lb2.setStyleSheet(u"color: rgb(255, 255, 255); ")
        iner_lb3.setStyleSheet(u"color: rgb(255, 255, 255); ")
        label.setStyleSheet(u"color: rgb(255, 255, 255); ")
        label.setAlignment(Qt.AlignCenter)
        iner_lb1.setFont(font)
        iner_lb2.setFont(font)
        iner_lb3.setFont(font)
        font.setFamily(u"Bahnschrift Light")
        label.setFont(font)
        font.setPointSize(14)
        
        in_from = QLineEdit()
        in_to = QLineEdit()
        in_from.setFont(font)
        in_to.setFont(font)
        in_from.setStyleSheet(u"background-color: rgb(255, 255, 255); border: 0px;")
        in_to.setStyleSheet(u"background-color: rgb(255, 255, 255); border: 0px;")
        in_from.setFixedSize(115, 20)
        in_to.setFixedSize(115, 20)
        
        hbox_for_inter.addWidget(iner_lb1)
        hbox_for_inter.addWidget(in_from)
        hbox_for_inter.addWidget(iner_lb2)
        hbox_for_inter.addWidget(in_to)
        hbox_for_inter.addWidget(iner_lb3)

        vbox_for_inter.addWidget(label)
        vbox_for_inter.addLayout(hbox_for_inter)
        inter_wid.setLayout(vbox_for_inter)
        inter_wid.setFixedWidth(327)

        hbox_for_inter2 = QHBoxLayout()
        hbox_for_inter2.addStretch(1)
        hbox_for_inter2.addWidget(inter_wid)
        hbox_for_inter2.addStretch(1)

        #Кнопки
        hbox_for_bnt = QHBoxLayout()

        btn_build = QPushButton()
        btn_build.setFixedSize(183, 41)
        btn_build.setText("Построить")
        btn_build.setFont(font)
        btn_build.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        btn_build.clicked.connect(lambda x: self.build_func(vbox_forInput, inter_wid))

        btn_ins = QPushButton()
        btn_ins.setFixedSize(183, 41)
        btn_ins.setText("Инструкция")
        btn_ins.setFont(font)
        btn_ins.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        btn_ins.clicked.connect(self.toIns)
        btn_wid = QWidget()
        btn_wid.setFixedHeight(75)
        hbox_for_bnt.addWidget(btn_build)
        hbox_for_bnt.addStretch(1)
        hbox_for_bnt.addWidget(btn_ins)
        btn_wid.setLayout(hbox_for_bnt)

        #Размещение
        hbox = QHBoxLayout()  
        vbox = QVBoxLayout()

        vbox.addWidget(lblHello)
        vbox.addWidget(inputFuncAll)
        vbox.addStretch(1)
        vbox.addLayout(hbox_for_inter2)
        vbox.addWidget(btn_wid)


        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.inputWID.setLayout(hbox)

        self.lable_error = QLabel('Введены некорректные данные.', self.inputWID)
        font.setFamily(u"Bahnschrift Light")
        font.setPointSize(12)
        self.lable_error.setStyleSheet(u"color: rgb(255, 0, 0); background-color: rgba(0,0,0,0)")
        self.lable_error.setFont(font)
        self.lable_error.setGeometry(275,32, 250, 20)
        self.lable_error.hide()


    def initGraf(self):
        self.grafWID.setParent(self.main)
        self.grafWID.setGeometry(QRect(0,25,800,575))
        font = QFont()
        font.setFamily(u"Bahnschrift Light")
        font.setPointSize(18)

        #Кнопки
        hbox_for_bnt = QHBoxLayout()
        btn_back = QPushButton()
        btn_back.setFixedSize(183, 41)
        btn_back.setText("Назад")
        btn_back.setFont(font)
        btn_back.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        btn_back.clicked.connect(self.toInput)
        btn_save = QPushButton()
        btn_save.setFixedSize(183, 41)
        btn_save.setText("Сохранить .png")
        btn_save.setFont(font)
        btn_save.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        btn_save.clicked.connect(self.save)
        btn_wid = QWidget()
        btn_wid.setFixedHeight(75)
        hbox_for_bnt.addWidget(btn_back)
        hbox_for_bnt.addStretch(1)
        hbox_for_bnt.addWidget(btn_save)
        btn_wid.setLayout(hbox_for_bnt)

        self.out_graf = QFrame()
        self.out_graf.setFixedSize(750, 450)
        self.out_graf.setStyleSheet("border: 1px solid black")

        #Размещение
        hbox = QHBoxLayout()  
        vbox = QVBoxLayout()

        vbox.addWidget(btn_wid)
        vbox.addWidget(self.out_graf)
        vbox.addStretch(1)

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.grafWID.setLayout(hbox)


    def initIns(self):
        self.instructWID.setParent(self.main)
        self.instructWID.setGeometry(QRect(0,25,800,575))
        font = QFont()
        #Верхний текст
        lblins = QLabel('Инструкция:')
        font.setFamily(u"Bahnschrift Light")
        font.setPointSize(24)
        lblins.setFont(font)
        lblins.setAlignment(Qt.AlignCenter)

        #Приветственный текст
        text = '''Для построения графика введите вашу функцию в соответствующее окно и нажмите кнопку \"Построить\". Для ввода можно использовать числа, знаки арифметических операций - + / * , константы pi, exp, скобки \"()\", переменную \"х\",  для возведения числа в степень используйте знак ^, для разделения дробной и целой части используйте точку \".\"

            Вы можете указать интервал, на котором будут построены функции. При не заполнение этого поля интервал будет x = [ -10; 10 ].

            Чтобы построить график нескольких функций нажмите кнопку \"Добавить\", чтобы убрать лишнюю функцию, нажмите на красный крест у поля ввода. Вы можете выбрать цвет отображения функции на графике, для этого нажмите на кнопку с цветом.

            Функции с некорректным вводом будут отображаться красным.
             '''.replace('''    ''', '')


        lbltext = QLabel(text)
        font.setPointSize(14)
        lbltext.setFont(font)
        lbltext.setWordWrap(True)
        lbltext.setStyleSheet("margin: 10px")

        #Кнока назад
        btn = QPushButton()
        btn.setText("Назад")
        btn.setFixedSize(183, 41)
        font.setPointSize(18)
        btn.setFont(font)
        btn.setStyleSheet("QPushButton { color: #FFFFFF; background-color: rgb(104, 101, 255); border: none;}")
        hbox_for_btn = QHBoxLayout()
        btn.clicked.connect(self.toInput)
        btn_wid = QWidget()
        btn_wid.setFixedHeight(75)
        hbox_for_btn.addStretch(1)
        hbox_for_btn.addWidget(btn)
        btn_wid.setLayout(hbox_for_btn)

        #Размещение
        hbox = QHBoxLayout()  
        vbox = QVBoxLayout()

        vbox.addWidget(lblins)
        vbox.addWidget(lbltext)
        vbox.addStretch(1)
        vbox.addWidget(btn_wid)

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.instructWID.setLayout(hbox)

    input_count = 0
    def inputFunc(self, outWID):
        wid = QWidget()
        wid.setFixedSize(750, 54)
        wid.setStyleSheet('background-color: rgb(104, 101, 255);')
        self.input_count += 1
        #Текст
        label = QLabel(wid)
        font = QFont()
        font.setFamily(u"Bahnschrift SemiBold")
        font.setPointSize(18)
        label.setFont(font)
        label.setFixedSize(65,30)
        label.setStyleSheet(u"color: rgb(255, 255, 255); ")
        label.setText(f"<html><head/><body><p>F<span style=\" vertical-align:sub;\">{self.input_count}</span>(X)=</p></body></html>")

        #Ввод функции
        lineEdit = QLineEdit()
        lineEdit.setFixedSize(575,37)
        font.setFamily(u"Bahnschrift Light")
        lineEdit.setFont(font)
        lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255); border: 0px;")

        #Выбор цвета
        comboBox = QComboBox(self.inputWID)
        comboBox.addItem(QIcon(self.red_path), '')
        comboBox.addItem(QIcon(self.blue_path), '')
        comboBox.addItem(QIcon(self.green_path), '')
        comboBox.addItem(QIcon(self.yellow_path), '')
        comboBox.addItem(QIcon(self.purpl_path), '')
        comboBox.setIconSize(QSize(23, 23))
        comboBox.setMinimumSize(QSize(37, 37))
        comboBox.setMaximumSize(QSize(37, 37))
        comboBox.setFocusPolicy(Qt.NoFocus)
        comboBox.setCurrentIndex(0)
        comboBox.setItemDelegate(QStyledItemDelegate())
        comboBox.setStyleSheet('''
        QComboBox {
            padding: 7px;
            border: 0px;
            background-color: rgb(255, 255, 255);} 
        QComboBox::drop-down { 
            background: black; 
            width: 0px; 
            border: 0px;}
        ''')
        comboBox.setMinimumContentsLength(5)

        #Кнопка удаления
        pushButton = QPushButton()
        pushButton.setMinimumSize(QSize(37, 37))
        pushButton.setMaximumSize(QSize(37, 37))
        pushButton.setIcon(QIcon(self.exit_path))
        pushButton.setStyleSheet("icon-size: 37px;")
        index = outWID.count()-1
        pushButton.clicked.connect(lambda x: self.delFunc(outWID, wid))

        #Размещение
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(lineEdit)
        hbox.addWidget(comboBox)
        hbox.addWidget(pushButton)
        wid.setLayout(hbox)

        outWID.insertWidget(index,wid)


    def addFunc(self, outWID):
        # size = 0
        # for i in range(outWID.count()):
        #     item = outWID.itemAt(i)
        #     if item.widget().isVisible():
        #         size+=1
        # if size < 6:
        #     self.inputFunc(outWID)
        if outWID.count() < 6:
            self.inputFunc(outWID)

   
    def delFunc(self, outWID, index):
        # size = 0
        # for i in range(outWID.count()):
        #     item = outWID.itemAt(i)
        #     if item.widget().isVisible():
        #         size+=1
        # if size > 2:
        #     item = outWID.takeAt(index)
        #     item.widget().close()
        if outWID.count() > 2:
            for i in range(outWID.count()):
                try:
                    if outWID.itemAt(i).widget() == index:
                        item = outWID.takeAt(i)
                        item.widget().hide()
                except AttributeError:
                    continue


    def displayError(self, outWID, arr, inter=None):
        if inter != None:
            self.lable_error.show()
            inter.setStyleSheet("background-color:  #CB0000")
        if len(arr) > 0:
            self.lable_error.show()
            for i in arr:
                item = outWID.itemAt(i)
                item.widget().setStyleSheet('background-color: #CB0000')
            return True
        return False
        

    def hideError(self, outWID, inter):
        self.lable_error.hide()
        for i in range(outWID.count()-1):
            item = outWID.itemAt(i)
            if item.widget().isVisible():
                item.widget().setStyleSheet('background-color: rgb(104, 101, 255); border: none')
        inter.setStyleSheet("background-color: rgb(104, 101, 255)")
                

    def save(self):
        fname = QFileDialog.getSaveFileName(caption='Сохранить', directory=self.path)
        print(fname[0])
        if fname[0] != '':
            self.g.figur.savefig(fname[0])
        

    def build_func(self, outWID, inter):
        self.hideError(outWID, inter)
        self.g = Graf(outWID, inter)

        if self.g.flag_iter:
            self.displayError(outWID, self.g.errors, inter)
            return    

        if self.displayError(outWID, self.g.errors):
            return

        
        canvas = FigureCanvas(self.g.figur)
        
        canvas.setParent(self.out_graf)
        canvas.setGeometry(QRect(1,1,748,448))

        toolbar = NavigationToolbar(canvas, self.out_graf)
        toolbar.resize(300, 35)

        self.toGraf()

    def toGraf(self):
        self.inputWID.hide()
        self.instructWID.hide()
        self.helloWID.hide()
        self.name.setText("XYZ - График")
        self.grafWID.show()

    def toIns(self):
        self.inputWID.hide()
        self.grafWID.hide()
        self.helloWID.hide()
        self.name.setText("XYZ - Инструкция")
        self.instructWID.show()

    def toHello(self):
        self.inputWID.hide()
        self.instructWID.hide()
        self.grafWID.hide()
        self.name.setText("XYZ")
        self.helloWID.show()

    def toInput(self):
        self.instructWID.hide()
        self.grafWID.hide()
        self.helloWID.hide()
        self.name.setText("XYZ - Ввод")
        self.inputWID.show()


    prev_mous_mos = [0, 0]


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            pos = e.screenPos()
            x_m = pos.x()
            y_m = pos.y()
            x = self.pos().x()
            y = self.pos().y()
            if (x_m - x < 805 and x_m - x > 4) and \
                 (y_m - y < 30 and y_m -y > 4):
                 self.prev_mous_mos[0] = x_m
                 self.prev_mous_mos[1] = y_m
                 self.mouseEvent = True
    
    def mouseReleaseEvent(self, e):
        self.mouseEvent = False

    def mouseMoveEvent(self, e):
        if self.mouseEvent:
            pos = e.screenPos()
            x = self.pos().x()
            y = self.pos().y()
            x_m = pos.x()
            y_m = pos.y()
            dx = x_m - self.prev_mous_mos[0]
            dy = y_m - self.prev_mous_mos[1]
            self.move(x+dx,y+dy)
            self.prev_mous_mos[0] = x_m
            self.prev_mous_mos[1] = y_m

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    hw = HelloWin()
    sys.exit(app.exec_()) 