from mesa import Model
from Ejemplo_tutorial.agents import CovidAgent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
import  numpy as np
# imports para la generacion normal de la edad
import scipy.stats as ss
import numpy as np
import random

# Creacion de variables globales 

NO_CONTAGIADO = 0
CEPA_LEVE = 1
CEPA_MEDIA = 2
CEPA_AGRESIVA = 3

class MoneyModel(Model):
    "A model with some number of agents."

    def __init__(self, number_of_agents,porcentaje_libre_movimiento,capacidad_sanidad,contagios_iniciales,cepa_covid, width, height):
        
        # Inicializamos las variables de estado del modelo
        self.num_agents = number_of_agents
        self.porcentaje_libre_movimiento = porcentaje_libre_movimiento
        self.capacidad_sanidad = capacidad_sanidad
        self.cepa_covid = cepa_covid
        
        # Cambiamos a tipo de variable entera en funcion de la cepa para poder operar mejor
        if(cepa_covid == "Cepa leve"):
            self.cepa_covid = CEPA_LEVE
        elif(cepa_covid == "Cepa media"):
            self.cepa_covid = CEPA_MEDIA
        elif(cepa_covid == "Cepa agresiva"):
            self.cepa_covid = CEPA_AGRESIVA
        
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.contagios_iniciales = contagios_iniciales
        
        # Calculamos la barrera poblacional inicialmente contagiada
        barrera_contagios_inicial = (contagios_iniciales/100)*number_of_agents
        
        media = 0
        # Creamos todos los agentes, a los cuales les vamos a asignar una edad en funcion de una distribucion normal
        # ademas en funcion de la poblacion inicialmente contagiada, comenzaran con covid o no
        for i in range(self.num_agents):
            
            # generamos la edad en funcion de una distribucion normal entre 1 y 100
            x = np.arange(1, 100)
            xU, xL = x + 0.5, x - 0.5 
            prob = ss.norm.cdf(xU, scale = 3) - ss.norm.cdf(xL, scale = 3)
            prob = prob / prob.sum() # normalize the probabilities so their sum is 1
            nums = np.random.choice(x, size = 1, p = prob)
            
            media += nums
            
            # Evaluamos en funcion de la generacion si inician contagiados o no
            if(i > barrera_contagios_inicial):
                a = CovidAgent(i, self, tipo_contagio=NO_CONTAGIADO ,edad=nums,cepa_covid=self.cepa_covid)
            else:
                a = CovidAgent(i, self, tipo_contagio=self.cepa_covid ,edad=nums,cepa_covid=self.cepa_covid)
            print (nums,"ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp",)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                
                if(self.grid.is_cell_empty((x,y)) == True):
                    self.grid.place_agent(a, (x, y) )
                    break
            
    #def get_cepa(self):
    #   return int(self.cepa_covid)
        print (media/self.num_agents,"uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",)
    
    def step(self):
        "Advance the model by one step."
        self.schedule.step()
