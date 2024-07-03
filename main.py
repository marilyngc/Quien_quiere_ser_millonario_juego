import pygame, sys
from funciones.button_class import Button

from Archivos.parser_json import parsear_json
from Archivos.parser_csv import leer_archivos

from funciones.dibujar import dibujar_texto, dibujar_imagen, mostrar_ultima_ganancia, get_font
from funciones.funciones import *
from funciones.actualizar import actulizar_pantalla_preguntas, actualizar_pantalla_menu

from funciones.manejar_eventos import obtener_evento, obtener_evento_videojuegos, obtener_evento_comodines, obtener_evento_teclado

from package_input.inputs import determinar_formato_ganancia

pygame.init() # inicializado pygame
path_comodines = "Archivos\documentos\comodines2.csv"
path_preguntas ="Archivos\documentos\preguntas_respuestas.json"

## json
preguntas_respuestas = parsear_json(path_preguntas)

## csv
lista_pistas = leer_archivos(path_comodines)
# print(pistas)

## colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AZUL_CLARO = (0, 150, 255)

ANCHO_VENTANA = 1200
LARGO_VENTANA = 700
TAMAÑO_VENTANA = (ANCHO_VENTANA, LARGO_VENTANA)
ventana = pygame.display.set_mode(TAMAÑO_VENTANA) # pixeles

pygame.display.set_caption("Quien quiere ser millonario") # titulo de la ventana

# traigo la imagen
icono = pygame.image.load("imagenes\icono\icono_milonario.png")

# seteo el icono
pygame.display.set_icon(icono)

# creo imagen de la superficie
background = pygame.image.load("imagenes\Background.png")
background = pygame.transform.scale(background, (TAMAÑO_VENTANA))

background_jugar = pygame.image.load("imagenes\Background_jugar.jpg")
background_jugar = pygame.transform.scale(background_jugar, (TAMAÑO_VENTANA))

background_opciones = pygame.image.load("imagenes\opciones.png")
background_opciones = pygame.transform.scale(background_opciones, (TAMAÑO_VENTANA))


lista_ultima_ganancia = [0]
lista_usuario = [0]

def ganador(): #igual
    
    clock = pygame.time.Clock()
    lista_botones = ["Si","No"]
    boton = Button((450,400),lista_botones, 20,BLANCO, None,ROJO,"Horizontal","imagenes\Botones\Boton_xs.png")
    score = determinar_formato_ganancia(str(lista_ultima_ganancia[0]))
    while True:
        mouse_posicion = pygame.mouse.get_pos()
        actualizar_pantalla_menu(ventana, background,"GANASTE!",30,BLANCO, None,(550,100), boton)

        dibujar_texto(ventana,"Quieres jugar de nuevo?", 30, BLANCO, None,(550,300))
        mostrar_ultima_ganancia(score, ventana, (600,210))
        boton_clickeado = obtener_evento(boton,lista_botones ,ventana, mouse_posicion)
        if boton_clickeado == "Si":
            main_menu()
        elif boton_clickeado == "No":
            pygame.quit()  
            sys.exit()                 
    
        pygame.display.update()
        
        clock.tick(15)

def perdedor(): #igual
    
    clock = pygame.time.Clock()
    lista_botones = ["Si","No"]
    boton = Button((500,400),lista_botones, 20,BLANCO, None,ROJO,"Horizontal","imagenes\Botones\Boton_xs.png")
    score = determinar_formato_ganancia(str(lista_ultima_ganancia[0]))
    
    while True:
        mouse_posicion = pygame.mouse.get_pos()
        actualizar_pantalla_menu(ventana, background,"Perdiste!",30,BLANCO, None,(600,150), boton)

        dibujar_texto(ventana,"¿Quieres jugar de nuevo?", 30, BLANCO, None,(600,300))
        mostrar_ultima_ganancia(score, ventana, (600,210))
        boton_clickeado = obtener_evento(boton,lista_botones ,ventana, mouse_posicion)
        if boton_clickeado == "Si":
            main_menu()
        elif boton_clickeado == "No":
            pygame.quit()  
            sys.exit()                 
    
        pygame.display.update()
        
        clock.tick(15)

def video_juegos():
    #TODO ESTO LUEGO EN UNA FUNCION
    
    cantidad_preguntas = 0
    
    N = 1
    M = 9
    matriz_ganancias = [[0]*N for _ in range(M)]
    
    lista_comodines = ["Publico","50-50","Llamada"]
    # comodines
    comodin = Button((200,70),lista_comodines,10,BLANCO, None,ROJO, "Vertical",None)
    recurso_comodin = None
    
    lista_banderas = [True, True, True]

    lista_ultima_ganancia.pop(0)
    ultima_ganancia = 0
    
    clock = pygame.time.Clock()
    tiempo_inicial = pygame.time.get_ticks()
    
    while True:
        pregunta = obtener_preguntas_progresivas(preguntas_respuestas["videojuegos"],cantidad_preguntas)
        
        mouse_posicion = pygame.mouse.get_pos()
        
        if recurso_comodin == None:
            recurso_comodin = obtener_evento_comodines(comodin, pregunta, lista_pistas, lista_banderas, mouse_posicion, recurso_comodin)
        
        
        # dibujar_texto(ventana, lista_usuario[0],20,BLANCO, NEGRO, (10,10))
        actulizar_pantalla_preguntas(ventana, background,background_opciones, 10 ,BLANCO, None, pregunta, comodin, matriz_ganancias, recurso_comodin)
        
        evento = obtener_evento_videojuegos(pregunta, matriz_ganancias, mouse_posicion, cantidad_preguntas, ultima_ganancia)
        if evento == "correcta":
            tiempo_inicial = pygame.time.get_ticks()
            ultima_ganancia = determinar_ultima_ganancia(matriz_ganancias, lambda ganacia: ganacia != 0)
            recurso_comodin = None
            cantidad_preguntas += 1
            
        elif evento == "incorrecta":
            lista_ultima_ganancia.append(ultima_ganancia)
            perdedor()    
         
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = round((tiempo_actual - tiempo_inicial) * 0.001)
        
        if tiempo_transcurrido == 30:
            lista_ultima_ganancia.append(ultima_ganancia)
            perdedor()

        if cantidad_preguntas == len(preguntas_respuestas["videojuegos"]):
            ultima_ganancia = determinar_ultima_ganancia(matriz_ganancias,lambda ganancia: ganancia != 0) + 1
            lista_ultima_ganancia.append(ultima_ganancia)
            ganador()
        
        # mostrar contador
        dibujar_imagen(ventana,"imagenes\Background_contador.png",(600,70))
        dibujar_texto(ventana,str(tiempo_transcurrido),20,BLANCO, None,(600,70) )    
       
        pygame.display.update()
        
        clock.tick(15)
        

# def componentes(): #OPCIONAL
#     clock = pygame.time.Clock()
#     while True:
#         # menu_mouse_posicion = pygame.mouse.get_pos()
        
#         ventana.blit(background,(0,0)) 
#         dibujar_texto(ventana,"Estamos en componentes", 30, BLANCO, None,(550,100))
        
#         # EVENTOS
#         lista_eventos = pygame.event.get()
#         for evento in lista_eventos:
#             if evento.type == pygame.QUIT: # pregunto si presiono la X de la ventana
#                 pygame.quit()  
#                 sys.exit()     
    
#             elif evento.type == pygame.MOUSEBUTTONDOWN :
#                 pass
        
#         pygame.display.update()
#         clock.tick(15)
        
def jugar():
    clock = pygame.time.Clock()
    
    fuente = get_font(20)

    input_box = pygame.Rect(500,550,200,32) 

    
    color_activo = AZUL
    color_inactivo = ROJO
    color_actual = color_inactivo
    activo = True
    texto = "invitado"
    
    #Los botones se crean fuera del bucle principal para evitar recrearlos en cada iteración.
    lista_menu_jugar = ["VIDEO JUEGOS","REGRESAR"] #"COMPONENTES"
    
    boton = Button((600,250), lista_menu_jugar, 20, BLANCO,None, ROJO, "Vertical","imagenes\Botones\Boton_xl.png")
    
    fuente = get_font(20)
    while True:
        mouse_posicion = pygame.mouse.get_pos()
        
        actualizar_pantalla_menu(ventana, background,"Elige una categoria", 40, BLANCO, None,(600,120),boton)
        
        # texto = obtener_evento_teclado(ventana, texto, color_activo, color_inactivo, mouse_posicion, activo, color_actual, input_box) 

        # lista_eventos = pygame.event.get() 
        # for evento in lista_eventos: #pygame.event.get()
        #     if evento.type == pygame.QUIT: 
        #         pygame.quit()
        #         sys.exit()
        #     elif evento.type == pygame.MOUSEBUTTONDOWN: #presiono el boton del mouse 
        #         if input_box.collidepoint(mouse_posicion):
        #             activo = not activo #no activo
        #             pygame.draw.rect(ventana, color_actual, input_box,2)
        #         if activo:
        #             color_actual = color_activo
        #         else:
        #             color_actual = color_inactivo
                    
        #     elif evento.type == pygame.KEYDOWN:
        #         if activo:
        #             if evento.key == pygame.K_BACKSPACE:
        #                 texto = texto[:-1] #hasta el final menos 1
        #             elif evento.key == pygame.K_ESCAPE:
        #                 texto = ""
        #             elif evento.key == pygame.K_RETURN:
        #                 activo = not activo
        #                 if activo:
        #                     color_actual = color_activo
        #                 else:
        #                     color_actual = color_inactivo
        #             else:
        #                 texto += evento.unicode
                        
        # text_surface = fuente.render(texto, True, color_actual)
        # ventana.blit(text_surface,(input_box.x+5, input_box.y+5))
        
        # pygame.draw.rect(ventana, color_actual, input_box,2)
        
        # lista_usuario = [texto]
        
        boton_clickeado = obtener_evento(boton, lista_menu_jugar,   ventana, mouse_posicion)
        if boton_clickeado == "VIDEO JUEGOS":
            video_juegos()  
        # elif boton_clickeado == "COMPONENTES":
        #     componentes()   
        elif boton_clickeado == "REGRESAR":
            main_menu()    

        pygame.display.update()
        
        clock.tick(15)
        


def main_menu():
    clock = pygame.time.Clock()
    lista_botones = ["JUGAR","SALIR"]
    #Los botones se crean fuera del bucle principal para evitar recrearlos en cada iteración.
    boton = Button((600,300), lista_botones,30,BLANCO,None, ROJO, "Vertical","imagenes\Botones\Boton_xl.png")

    while  True: # blucle infinito
        menu_mouse_posicion = pygame.mouse.get_pos()
        actualizar_pantalla_menu(ventana, background, "Bienvenido!", 60, BLANCO, None,(600,120),boton)
        
        # EVENTOS
        boton_clickeado = obtener_evento(boton, lista_botones ,ventana, menu_mouse_posicion)
        if boton_clickeado == "JUGAR":
            jugar()
        elif boton_clickeado == "SALIR":
            pygame.quit()  
            sys.exit()                 
            
        pygame.display.update()
        clock.tick(15)
    
main_menu()          
        