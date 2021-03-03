import pygame
import os

lysol = pygame.image.load(os.path.join('recursos', 'lysolMod.png'))
covid = pygame.image.load(os.path.join('recursos', 'covid19Mod.png'))

class Cuadricula:
    def __init__(self):
        self.linea_cuadricula = [((0,200),(600,200)),
                                 ((0,400),(600,400)),
                                 ((200,0),(200,600)),
                                 ((400,0),(400,600))]

        self.cuadricula = [[0 for x in range(3)] for y in range(3)]

        self.cambio_jugador = True

        #DIRECCIONES                N       NO      O       SO    S     SE    E     NE
        self.busqueda_direccion = [(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)]

        self.fin_juego = False


    def dibujar(self,pantalla):
        for linea in self.linea_cuadricula:
            pygame.draw.line(pantalla, (200,200,200), linea[0], linea[1], 2)

        for y in range(len(self.cuadricula)): #Elementos de afuera
            for x in range(len(self.cuadricula[y])): #Elementos por dentro
                if self.get_celda(x,y) == "Lysol":
                    pantalla.blit(lysol, (x*200, y*200))
                elif self.get_celda(x,y) == "Corona":
                    pantalla.blit(covid, (x*200, y*200))


    def print_cuadricula(self):
        for fila in self.cuadricula:
            print(fila)

    def get_celda(self, x, y):
        return self.cuadricula[y][x]

    def set_celda(self, x, y, valor):
        self.cuadricula[y][x] = valor

    def get_mouse(self, x, y, jugador):
        if self.get_celda(x,y) == 0:
           self.set_celda(x,y,jugador)
           self.check_cuadricula(x, y, jugador)


    def entre_limite(self, x,y,):
        return x >= 0 and x < 3 and y >= 0 and y < 3

    def cuadricula_llena(self):
        for fila in self.cuadricula:
            for valor in fila:
                if valor == 0:
                    return False
        return True

    def check_cuadricula(self, x,y,jugador):
        count = 1
        for index, (dirx,diry) in enumerate(self.busqueda_direccion):
            if self.entre_limite(x+dirx, y+diry) and self.get_celda(x+dirx, y+diry) == jugador:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.entre_limite(xx+dirx, yy+diry) and self.get_celda(xx+dirx, yy+diry) == jugador:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    nuevo_dir = 0
                    if index == 0:
                        nuevo_dir = self.busqueda_direccion[4]
                    elif index == 1:
                        nuevo_dir = self.busqueda_direccion[5]
                    elif index == 2:
                        nuevo_dir = self.busqueda_direccion[6]
                    elif index == 3:
                        nuevo_dir = self.busqueda_direccion[7]
                    elif index == 4:
                        nuevo_dir = self.busqueda_direccion[0]
                    elif index == 5:
                        nuevo_dir = self.busqueda_direccion[1]
                    elif index == 6:
                        nuevo_dir = self.busqueda_direccion[2]
                    elif index == 7:
                        nuevo_dir = self.busqueda_direccion[3]

                    if self.entre_limite(x+nuevo_dir[0], y+nuevo_dir[1])\
                        and self.get_celda(x+nuevo_dir[0], y+nuevo_dir[1]) == jugador:

                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            print(jugador, 'Ganador')
            self.fin_juego = True
        else:
            self.fin_juego = self.cuadricula_llena()


    def clear_cuadricula(self):
        for y in range(len(self.cuadricula)):
            for x in range(len(self.cuadricula[y])):
                self.set_celda(x,y,0)






