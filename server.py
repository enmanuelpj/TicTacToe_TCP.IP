import pygame
import os
from cuadricula import Cuadricula

os.environ['SDL_VIDEO_WINDOW_POSITION'] = '200,100'

pantalla = pygame.display.set_mode((600,600))
pygame.display.set_caption('Lysol-Mata-Corona')

import threading

def create_thread(target):
    thread = threading.Thread(target = target)
    thread.daemon = True
    thread.start()



import socket

HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn,addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4,TCP
sock.bind((HOST, PORT))
sock.listen(1)

def recieve_data():
    global  turno
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'TuTurno':
            turno = True
        if data[3] == 'False':
            cuadricula.fin_juego = True
        if cuadricula.get_celda(x, y) == 0:
            cuadricula.set_celda(x, y, 'Corona')
        print(data)


def waiting_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept()  # aceptara la coneccion. Esperara a la coneccion, esta bloqueando el metodo(hilo principal)
    print('El cliente esta conectado')
    connection_established = True
    recieve_data()

create_thread(waiting_connection)

cuadricula = Cuadricula()


ejecucion = True
jugador = "Lysol"
turno = True
jugando = 'True'


while ejecucion:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecucion = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if turno and not cuadricula.fin_juego:
                    posicion = pygame.mouse.get_pos()
                    celdaX, celdaY = posicion[0]//200, posicion[1]//200
                    cuadricula.get_mouse(celdaX, celdaY, jugador)
                    if cuadricula.fin_juego:
                        jugando = 'False'
                    send_data = '{}-{}-{}-{}'.format(celdaX,celdaY, 'TuTurno', jugando).encode()
                    conn.send(send_data) #Creado cuando se crea el cliente
                    turno = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and cuadricula.fin_juego:
                cuadricula.clear_cuadricula()
                cuadricula.fin_juego = False
                jugando = 'True'
            elif event.key == pygame.K_ESCAPE:
                ejecucion = False


    pantalla.fill((0,0,0))

    cuadricula.dibujar(pantalla)

    pygame.display.flip()



