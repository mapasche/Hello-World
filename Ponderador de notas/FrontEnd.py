from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal
import sys
import os
from BackEnd import PonderadorNotas


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



main_window, main_window_class = uic.loadUiType(resource_path('Main.ui'))

class  MainWindow (main_window, main_window_class):
    
    senal_enviar_datos = pyqtSignal(list, int)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ramos = list()
        self.contador = 0
        
    def agregar_ramos(self):
        num_ramos = len(self.ramos)
        ramo = RamoLayout(self.senal_enviar_datos, self.contador)
        self.contador += 1
        self.ramos.append(ramo)
        
        self.verticalLayout.insertLayout(num_ramos * 2 + 3, ramo)
        self.verticalLayout.insertStretch(num_ramos * 2 + 4)
        
        self.update()
        
        
    def notas (self, nota_ponderada, nota_pasar, ide):
        ramo = None
        for layout in self.ramos:
            if layout.id == ide:
                ramo = layout
                break
            
        total_notas = len(ramo.notas)

        layout_text = ramo.itemAt(total_notas + 2).layout()
        
        label_pond = layout_text.itemAt(1).widget()

        label_nota = layout_text.itemAt(3).widget()

        label_pond.setText("Poderacion nota: " + str(nota_ponderada))
        label_nota.setText("Nota requeridas: " + str(nota_pasar))
        self.update()
    
    
class RamoLayout(QHBoxLayout):
    
    def __init__(self, senal_enviar, ide, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.notas = list()
        self.senal_enviar = senal_enviar
        self.id = ide
        
        self.addStretch()
        
        vnotas = NotaLayout()
        self.notas.append(vnotas)
        
        self.addLayout(vnotas)
        self.addStretch()
        
        vnotas = QVBoxLayout()
        vnotas.addStretch() 
        vnotas.addWidget(QLabel('Poderacion nota: '))
        vnotas.addStretch()
        vnotas.addWidget(QLabel('Nota requeridas: '))
        vnotas.addStretch()
        
        self.addLayout(vnotas)
        self.addStretch()
        
        vnotas = QVBoxLayout()
        vnotas.addStretch()
        boton = QPushButton('Calcular')
        boton.clicked.connect(self.calcular)
        vnotas.addWidget(boton)
        boton = QPushButton('Añadir Nota')
        boton.clicked.connect(self.anadir_nota)
        vnotas.addWidget(boton)

        mini_lay = QHBoxLayout()
        boton = QPushButton('Reiniciar')
        boton.clicked.connect(self.reiniciar)
        mini_lay.addWidget(boton)

        boton = QPushButton('Borrar Nota')
        boton.clicked.connect(self.borrar)
        mini_lay.addWidget(boton)

        vnotas.addLayout(mini_lay)
        vnotas.addStretch() 
        
        self.addLayout(vnotas)
        self.addStretch()
            
        
    def anadir_nota (self):
        
        vnotas = NotaLayout()
        self.notas.append(vnotas)
        self.insertLayout(len(self.notas), vnotas)
        
    
    def calcular(self):
        #obtener valores
        l_ponderaciones = list()
        l_notas = list()
        for i in self.notas:
            l_ponderaciones.append(i.itemAt(1).widget().text())
            l_notas.append(i.itemAt(3).widget().text())
            
        self.senal_enviar.emit(list(zip(l_ponderaciones, l_notas)), self.id)
    
    
    def reiniciar(self):

        for i in self.notas:
            i.itemAt(1).widget().setText("")
            i.itemAt(3).widget().setText("")


    def borrar(self):

        if len(self.notas) > 0:

            child = self.takeAt(1)
            self.notas.remove(child)

            while child.layout().count():

                child_child = child.layout().takeAt(0)
                    
                if child_child.widget():
                    child_child.widget().deleteLater()
                
                elif child_child.spacerItem():
                    child.layout().removeItem(child_child)
                    del child_child

                else:
                    raise Exception("Error con los objetos del layout")

            del child
                
            self.update()

    
          
        
class NotaLayout(QVBoxLayout):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.addStretch()
        linea_edit = QLineEdit('')
        linea_edit.setPlaceholderText("%")
        self.addWidget(linea_edit)
        self.addStretch()
        linea_edit = QLineEdit('')
        linea_edit.setPlaceholderText("70")
        self.addWidget(linea_edit)
        self.addStretch()





"""
def borrar_layout(layout):
    print(layout)
    while layout.count():
        child = layout.takeAt(0)

        if child.layout():
            borrar_layout(child.layout())
            
        elif child.widget():
            child.widget().deleteLater()
        
        elif child.spacerItem():
            layout.removeItem(child)
            del child

        else:
            raise Exception("Error con los objetos del layout")
    
    del layout
    return    
"""








if __name__ == "__main__":
    
    def hook(type, value, traceback):
        print(type)
        print(traceback)
        sys.__except__ = hook


    
    
    app = QApplication([])
    main_widget = MainWindow()
    ponderador = PonderadorNotas()
    
    
    #Unir senales
    main_widget.senal_enviar_datos.connect(ponderador.recibir_datos)
    ponderador.senal_notas.connect(main_widget.notas)
    
    #iniciar    
    main_widget.show()
    sys.exit(app.exec_())
