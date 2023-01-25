# TRABAJO REALIZADO POR:
#   Jose Luis Rico Ramos
#   Miguel Tirado Guzmán
#


from mesa import Agent
import numpy

NO_CONTAGIADO = 0
CEPA_LEVE = 1
CEPA_MEDIA = 2
CEPA_AGRESIVA =3

LIBRE_MOVIMIENTO = 0
NO_MOVILIDAD = 1

# Probabilidades de contagio en funcion de la variante covid
PROB_CONTAGIO_VARIANTE = numpy.array([0.0,0.2,0.4,0.6])

PROB_MUERTE_VARIANTE = numpy.array([0.0,0.005,0.01,0.015])


# Probabilidades de contagio extra en funcion de la edad
# Para el codigo simplemente dividiremos la edad entre 10 y nos 
# indicará la posición del vector a la que tenemos que ir.
PROB_CONTAGIO_EDAD = numpy.array([0.05,0.1,0.15,0.2,0.25,0.35,0.45,0.5,0.55,0.6])


# Probabilidades de muerte en funcion de la edad
# Para el codigo simplemente dividiremos la edad entre 10 y nos 
# indicará la posición del vector a la que tenemos que ir.
PROB_MUERTE_EDAD = numpy.array([0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01])


# Tiempo contagiado en funcion de la variante covid
TIEMPO_CONTAGIO = numpy.array([0,7,10,12])
PROBABILIDAD_CURA = numpy.array([0,0.30,0.20,0.10])

class CovidAgent(Agent):

    # Constrcutor de nuestro agente, en el que le daremos valor a cada una de las variables de clase
    def __init__(self, unique_id, model, tipo_contagio, edad, cepa_covid, movimiento):
        super().__init__(unique_id, model)
        self.tipo_contagio = int(tipo_contagio)
        self.edad = edad
        self.duracion_contagio = 0
        self.cepa_covid = int(cepa_covid)
        self.libre_movimiento = movimiento


    # funcion por frames del modelo, donde se ejecutara en cada una de las etapas
    #La funcion es simple:
    #1. Evaluamos si el agente es de los que tienen libertad de movimiento, si es así se mueve
    #2. Si no estaba contagiado miramos si se contagia en la nueva posición
    #3. Si estaba contagiado miramos si fallece o se cura
    def step(self):
        if(self.libre_movimiento == LIBRE_MOVIMIENTO):
            self.move()
        if self.tipo_contagio == 0:
            self.contagiarse()
        else:
            self.fallecer()
            self.curarse()
    
    # funcion en la que comprobamos si se va a contagiar el nuevo agente o no
    def contagiarse(self):
        # nos recorremos cada uno de los agentes de las celdas de al rededor
        for agente in self.model.grid.get_neighbors(self.pos,True):
            
            if(agente.tipo_contagio != NO_CONTAGIADO ):
                
                # calculamos la probabilidad de haberse contagiado con este contacto en concreto
                # sumamos en funcion de la edad la % de contagio y de la variante
                # probabilidad_contagio = PROB_CONTAGIO_VARIANTE[self.cepa_covid] + PROB_CONTAGIO_EDAD[round(self.edad/10)]

                # La probabilidad de contagio se ve aumentada un % en función de la edad
                

                # comprobamos la casilla en la que se encuentra para sumar o reducir la posibilidad de contagio
                # teniendo en cuenta que no es lo mismo encontrarse en una diagonal que al lado
                
                # si la diferencia entre las posiciones es 0, 2 o -2 son diagonales, se trata de celdas adyacentes y si no se trata de diagonales
                if( (self.pos[0]+self.pos[1])-(agente.pos[0]+agente.pos[1]) == 0 
                    or (self.pos[0]+self.pos[1])-(agente.pos[0]+agente.pos[1]) == 2
                    or (self.pos[0]+self.pos[1])-(agente.pos[0]+agente.pos[1]) == -2):
                    #Este es el caso de celdas DIAGONALES
                    # probabilidad_contagio += 0.1
                    # Lo multiplicamos por 0.95 porque así tiene decrecen las probabilidades en un 5%
                    probabilidad_contagio = PROB_CONTAGIO_VARIANTE[self.cepa_covid] *(1 +  PROB_CONTAGIO_EDAD[round(self.edad/10)])*0.95
                else:
                    #Caso de las celdas NO DIAGONALES
                    probabilidad_contagio = PROB_CONTAGIO_VARIANTE[self.cepa_covid] *(1 +  PROB_CONTAGIO_EDAD[round(self.edad/10)])*1.1
                
                # si el numero aleatorio entre 0 y 1 sale menor se cumple la probabilidad
                probabilidad_efeciva = self.random.random()
                if( probabilidad_efeciva < probabilidad_contagio):
                    #Si finalmente se contagia, lo registramos
                    self.model.no_contagiados = self.model.no_contagiados - 1
                    self.model.contagiados = self.model.contagiados + 1
                    self.tipo_contagio = agente.tipo_contagio
    
    # Si esta contagiado, comprobamos si ya se ha curado o no
    def curarse(self):
        #Calculamos la probabilidad de cura, la cual es una funcion exponencial al tiempo que lleva
        # contagiado y también se ve afectada por la capacidad neta de la sanidad en ese momento.
        probabilidad_cura = ((1+PROBABILIDAD_CURA[self.cepa_covid])**(self.duracion_contagio - TIEMPO_CONTAGIO[self.tipo_contagio])-1)

        # Si fuesen iguales estaríamos exponiendo a 0 y al sumar 1 la probabilidad es de 1
        if(self.duracion_contagio == TIEMPO_CONTAGIO[self.tipo_contagio]):
            probabilidad_cura =PROBABILIDAD_CURA[self.cepa_covid]


        probabilidad_cura = probabilidad_cura + (probabilidad_cura * (self.model.capacidad_neta()))

        # En funcion del tipo de contagio el tiempo de duracion no es el mismo, por lo que comprobamos  que ya ha pasado el tiempo 
        # suficiente contagiado, como para curarse, accediendo al vectror de TIEMPO_CONTAGIO, donde se almacena el tiempo que ha 
        # de estar cada agente contagiado antes de curarse
        if (self.duracion_contagio > TIEMPO_CONTAGIO[self.tipo_contagio] and self.random.random() < (probabilidad_cura)):
            self.model.no_contagiados = self.model.no_contagiados + 1
            self.model.contagiados = self.model.contagiados-1
            self.tipo_contagio = 0
            self.duracion_contagio = 0
        else:
            self.duracion_contagio = self.duracion_contagio + 1 
    
    # Comprobamos con esta funcion en cada iteracion si el agente va a morirse o no, en caso de que la probabilidad ponderada, 
    # por la edad, por el tipo de cepa, el agente puede  morirse y desaparecer del modelo
    def fallecer(self):
        prob_fallecer = (1+PROB_MUERTE_EDAD[round(self.edad/10)])*(1+PROB_MUERTE_VARIANTE[self.tipo_contagio])-1
        
        probabilidad_efeciva = self.random.random()
        if(probabilidad_efeciva<prob_fallecer):
            self.model.n_fallecidos = self.model.n_fallecidos+1
            self.model.contagiados = self.model.contagiados-1
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    # Creamos la funcion de movimiento de los agentes de forma aleatoria
    def move(self):
        # Guardamos en una lista las posibles casillas a las que se podria dirigir el agente
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False )
                
        # Comprobamos que haya alguna casilla en esa lista de no ocupada
        if(len(possible_steps) > 0):
            
            new_position = self.random.choice(possible_steps)
            
            # Comprobamos que la celda a la que nos vamos a mover este libre, ya que trabajamos con un SingleGrid
            if(self.model.grid.is_cell_empty(new_position) == True):
                self.model.grid.move_agent(self, new_position)
        if(len(possible_steps)==0):
            print("No puedo moverme")
