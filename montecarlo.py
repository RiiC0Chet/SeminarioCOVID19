import numpy as np
import xlsxwriter
import pandas as pd
import math
from math import exp
import openpyxl
from Ejemplo_tutorial.model import MoneyModel
#importamos los datos del excel en el que tenemos los datos de chile reales
#datos = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Mundo_en_cifras/El_Mundo_en_Cifras_13_12_2022_16_35_23.xlsx', skiprows=7 , names= ['Año', 'Atdatos', 'RRtdatos', 'Cftdatos', 'Ydtdatos'])
#creamos las variables con los datos del excel de Chile

# global Pt_chile
# Pt_chile = datos['Pt_chile0']
# global At_chile
# At_chile = datos['At_chile1']
# global RRt_chile
# RRt_chile = datos['RRt_chile2']
# gobal Cft_chile
# Cft_chile = datos['Cft_chile3']
# global Ydt_chile
# dt_chile = datos['Ydt_chile4']

n_ciudadanos = []
libre_movimiento = []
poblacion_contagios = []
capacidad_sanidad = []
tipo_cepa = []

NUM_MUESTRAS = 100
for i in range (NUM_MUESTRAS):
    n_ciudadanos.append(np.random.randint(150,200))
    libre_movimiento.append(np.random.randint(1,100))
    poblacion_contagios.append(np.random.randint(1,100))
    capacidad_sanidad.append(np.random.randint(1,100))
    tipo_cepa.append(np.random.randint(1,3))


#establecemos los valores de las variables que vamos a utilizar durante la ejecución del código
a0 = 1 #a0 > 0
a2 = 1 #a2 > 0
a1 = -0.1 #a1 < 0
a3 = -1 #a3 < 0
alpha = -0.1 #alpha < 0
n = 0.5 #entre 0 y 1
sigma_cuadrado = 1
beta = 1
L = 12
K = 12
gamma = 1
b0 = 1
b1 = 1
b2 = -0.1
class Montecarlo():
    def __init__(self) -> None:
        self.Rvt_todos()
        #self.todos_montecarlo()


    #Esta función crea un archivo excel donde almacenará todos los datos que vaya creando para montecarlo
    #Generará datos aleatorios para Pt_chile, Ydt_chile, RRt_chile, Cft_Chile y At_Chile
    def montecarlo(self, nombre_archivo):
        libro = xlsxwriter.Workbook(nombre_archivo)
        hoja = libro.add_worksheet()
        col =0
        #aleatorios_Pt_chile1 = np.random.normal(Pt_chile.mean(),np.sqrt(Pt_chile.var()),Pt_chile.size)
        row = 0
        hoja.write(row,col, 'n_ciudadanos'+str(col))
        # Iteramos los datos para ir pintando fila a fila
        for dato in (n_ciudadanos):
            hoja.write(row+1, col, dato)
            row += 1

        #generamos los datos de montecarlo para At
        col += 1
        #aleatorios_At_chile1 = np.random.normal(At_chile.mean(),np.sqrt(At_chile.var()),At_chile.size)
        row = 0
        hoja.write(row,col, 'libre_movimiento'+str(col))
        # Iteramos los datos para ir pintando fila a fila
        for dato in (libre_movimiento):
            hoja.write(row+1, col, dato)
            row += 1

        #generamos los datos de montecarlo para RRt
        col += 1
        #aleatorios_RRt_chile1 = np.random.normal(RRt_chile.mean(),np.sqrt(RRt_chile.var()),RRt_chile.size)
        row = 0
        hoja.write(row,col, 'poblacion_contagios'+str(col))
        # Iteramos los datos para ir pintando fila a fila
        for dato in (poblacion_contagios):
            hoja.write(row+1, col, dato)
            row += 1

        #generamos los datos de montecarlo para Cft
        col += 1
        #aleatorios_Cft_chile1 = np.random.normal(Cft_chile.mean(),np.sqrt(Cft_chile.var()),Cft_chile.size)
        row = 0
        hoja.write(row,col, 'capacidad_sanidad'+str(col))
        # Iteramos los datos para ir pintando fila a fila
        for dato in (capacidad_sanidad):
            hoja.write(row+1, col, dato)
            row += 1

        #generamos los datos de montecarlo para Ydt
        col += 1
        #aleatorios_Ydt_chile1 = np.random.normal(Ydt_chile.mean(),np.sqrt(Ydt_chile.var()),Ydt_chile.size)
        row = 0
        hoja.write(row,col, 'tipo_cepa'+str(col))
        # Iteramos los datos para ir pintando fila a fila
        for dato in (tipo_cepa):
            hoja.write(row+1, col, dato)
            row += 1

        #Cerramos el libro
        libro.close()

    #Genera las 10 muestras necesarias para Montecarlo
    def todos_montecarlo(self):
        for i in range(10):
            self.montecarlo("Montecarlo_covid"+str(i)+".xlsx")




    # #Calculamos el valor del retorno esperado de invertir en un período dado
    # #Ecuación 22 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    # def calcular_retorno_esperada_inversion(self,mes_actual):
    #     Rt1 = (a0 - b0) + (a1 - b1) * Pt_chile[mes_actual] + a2 * Ydt_chile[mes_actual]  + a3 * RRt_chile[mes_actual] + b2 * Cft_chile[mes_actual] + self.calcular_Wt(mes_actual) * (float(alpha) * (Pt_chile[mes_actual] - self.calcular_valor_fundamental_precios_vivienda(mes_actual))) + (1 - self.calcular_Wt(mes_actual))*self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual) + self.calcular_ruido_blanco()
    #     return Rt1

    # #Calculamos el valor de los errores de predicción de los inversores fundamentalistas para el mes actual
    # #Ecuación 13 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    # def  calcular_errores_prediccion_fundamentalistas(self,mes_actual):
    #     eft = 0
    #     for i in range(K) :
    #         eft += abs( alpha * (Pt_chile[mes_actual - i] - self.calcular_valor_fundamental_precios_vivienda(mes_actual-i)) - (Pt_chile[mes_actual +1]-Pt_chile[mes_actual]))
    #     return eft

    # #Calculamos el valor de los errores de predicción de los inversores psicológicos para el mes actual
    # #Ecuación 14 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    # def  calcular_errores_prediccion_psicologicos(self, mes_actual):
    #     est = 0
    #     for i in range(K) :
    #         est += abs(self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual- i+1) - (Pt_chile[mes_actual-i +1]-Pt_chile[mes_actual-i]))
    #     return est


    # #Calculamos el valor de Wt para el mes actual. Siendo Wt el peso relativo que tienen los fundamentalistas en el periodo t.
    # #   Tendremos un valor de Wt entre 0 y 1
    # #Ecuación 12 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    # def  calcular_Wt(self,mes_actual):
    #     Wt= 1 / (1 + exp(gamma * ((self.calcular_errores_prediccion_fundamentalistas(mes_actual) - self.calcular_errores_prediccion_psicologicos(mes_actual)) / (self.calcular_errores_prediccion_fundamentalistas(mes_actual) + self.calcular_errores_prediccion_psicologicos(mes_actual)))))
    #     return Wt

    # #Calculamos el valor de g, que es el valor de la tasa de crecimiento de las rentas. Asumimos que es el promedio del crecimiento mensual de los índices de precios de los arriendos
    # def  calcular_g(self):
    #     suma = 0
    #     for i in range(At_chile.size - 1):
    #         suma += At_chile[i+1] - At_chile[i]

    #     g= suma/ (At_chile.size - 1)
    #     return g

    # #Calculamos el valor fundamental de la vivienda en cada periodo
    # #Ecuación 6 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    # def  calcular_valor_fundamental_precios_vivienda(self,mes_actual):
    #     Fvt = ((1 + self.calcular_g()) * At_chile[mes_actual] ) / (At_chile[mes_actual] / Pt_chile[mes_actual])
    #     return Fvt


    # #Calculamos el valor de las ganancias esperadas por los inversores psicológicos para el mes actual
    # #Ecuación 8 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    # def  calcular_ganancias_esperadas_inversores_psicologicos_Rt1(self,mes_actual):
    #     suma = 0
    #     for i in range(L) :
    #         suma += (Pt_chile[mes_actual -i ]-Pt_chile[mes_actual-i -1])
    #     Et_psicologicos_Rt1= suma * beta
    #     return Et_psicologicos_Rt1
    
    def mse(self,vec1, vec2):
        return sum((np.array(vec1) - np.array(vec2))**2) / len(vec1)

    def Rvt_todos(self):
        menor_error = 9999999999999999
        row_ = 0
        
        #contagios_reales = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Mundo_en_cifras/El_Mundo_en_Cifras_13_12_2022_16_35_23.xlsx', skiprows=7 , names= ['España'])
        # Abrir el archivo XLSX
        wb = openpyxl.load_workbook('cifras_contagios.xlsx')

        # Seleccionar la hoja de trabajo que queremos leer
        ws = wb['Hoja1']

        # Crear una lista para almacenar los valores leídos
        contagios_reales = []

        # Iterar a través de las 40 primeras filas de la columna "España"
        for row in ws['C2:C41']:
            # Agregar el valor de la celda a la lista
            contagios_reales.append(row[0].value)
        #print(contagios_reales)
        # Cerrar el archivo XLSX
        wb.close()

        for i in range (NUM_MUESTRAS):
            modelo = MoneyModel(n_ciudadanos[i],
                                        libre_movimiento[i],
                                        capacidad_sanidad[i],
                                        poblacion_contagios[i],
                                        tipo_cepa[i],20,20)
            contagios_simulacion=[]
            for j in range (40):
                modelo.step()
                contagios_simulacion.append(modelo.current_non_healthy_agents(modelo) *(47000000/n_ciudadanos[i])) 
            error_cuad = self.mse(contagios_simulacion, contagios_reales)
            if(menor_error > error_cuad):
                menor_error = error_cuad
                row_ = i
            #print(error_cuad , i)
            
        print ("Numero ciudadanos: " , n_ciudadanos[row_] ,"Porcentaje libre movimiento: " ,  libre_movimiento[row_], "Capacidad sanidad: " , capacidad_sanidad[row_], "Poblacion inicialmente contagiada: " ,poblacion_contagios[row_], "Tipo de cepa: ",tipo_cepa[row_], "Iteracion donde se consigue: ", row_)

ejecutar = Montecarlo()