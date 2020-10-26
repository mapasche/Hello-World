#BackEnd
from PyQt5.QtCore import QObject, pyqtSignal
from functools import reduce
import math

class PonderadorNotas(QObject):
    
    senal_notas = pyqtSignal(float, float, int)
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.__nota_minima = 39.5
    
    
    def recibir_datos(self, l_notas, ide):            
            
        l_notas_corregido = list()
        try:
            for tupla in l_notas:
                if not tupla[0].isdecimal():
                    raise Exception("Ponderacion no es numerica")
                
                if not tupla[1].isdecimal() and tupla[1] != "":
                    
                    raise Exception("Nota no es numerica o vacia")
                    
                elif tupla[1] == "":
                    
                    l_notas_corregido.append((int(tupla[0]), -1))
                    
                else:
                    
                    l_notas_corregido.append((int(tupla[0]), int(tupla[1])))
                    
                
        except Exception as error:
            print("Error: ", error)
            
        else:
            
            ponderacion_total = reduce(lambda x,y: x + y[0], l_notas_corregido, 0)
            if ponderacion_total != 100:
                print("Error, ponderacion no suma 100")
                ########################################################                
                
            else:
                nota_ponderada = self.obtener_nota_ponderada(l_notas_corregido)
                nota_pasar = self.obtener_nota_pasar(l_notas_corregido)
                
                self.senal_notas.emit(nota_ponderada, nota_pasar, ide)
        
        
    def obtener_nota_ponderada(self, notas):
        suma_ponderacion = float()
        nota = float()
        
        for conjunto in notas:
            if conjunto[1] == -1:
                pass
            else:
                nota += conjunto[0] * conjunto[1]
                suma_ponderacion += conjunto[0]
        
        nota_ponderada = nota / suma_ponderacion
        nota_ponderada = self.round_half_up(nota_ponderada, 1)
        return nota_ponderada


                
        
    def obtener_nota_pasar(self, notas):
        
        nota_decimal = float()
        ponderacion_decimal = float()
        
        for conjunto in notas:
            if conjunto[1] == -1:
                pass
            else:
                ponderacion = conjunto[0] / 100
                nota_decimal += ponderacion * conjunto[1]
                ponderacion_decimal += ponderacion

        try:
            nota_pasar = (self.__nota_minima - nota_decimal) / (1 - ponderacion_decimal)
        except ZeroDivisionError:
            nota_pasar = self.__nota_minima - nota_decimal
        return self.round_half_up(nota_pasar, 1)

        
        
                
        
    def round_half_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier
            
