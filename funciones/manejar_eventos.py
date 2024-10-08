import pygame
import sys
from .dibujar import get_font
from package_input.inputs import verificar_ingreso_datos
from .button_class import Button
from .pregunta_class import Pregunta

def obtener_evento(boton:Button, mouse_posicion:tuple) -> Button | None :  
    """Obtener evento

    Args:
        boton (button_class): un boton determinado como objeto
        mouse_posicion (tuple): coordenadas del mouse 

    Returns:
        Button|None: Button en caso de apretar el boton | None en caso de que no se clickee una opcion 
    """
    retorno = None
    boton_clickeado = boton.capturar_mouse_movimiento(mouse_posicion)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            
            if boton_clickeado:
                retorno = boton_clickeado
      
    return retorno

def obtener_evento_comodines(comodin:Button, pregunta:Pregunta, lista_pistas:list[dict], lista_banderas:list[tuple], mouse_posicion:tuple, recurso:str) -> list: 
    """Obtener el evento de comodines

    Args:
        comodin (Button): comodin como objeto
        pregunta (Pregunta): pregunta como objeto
        lista_pistas (list[dict]): lista de diccionarios con las preguntas y pistas
        lista_banderas (list[tuple]): lista con tuplas para un solo uso de los comodines
        mouse_posicion (tuple): coordenadas del mouse 
        recurso (list): string vacio 

    Returns:
        list: lista con el recurso y el nombre del comodin
    """
    lista_porcentaje = []
    porcentajes = 0
   
    comodin_elegido = pygame.mouse.get_pressed() #
    
    if comodin_elegido[0]:
        comodin_clickeado = comodin.capturar_mouse_movimiento(mouse_posicion)
        
        if comodin_clickeado == "Imagen 2" and verificar_ingreso_datos(lista_banderas[0]):
            pista = pregunta.obtener_pista(lista_pistas)
            lista_banderas[0] = False
            recurso = [pista,"Llamada"]
            
        elif comodin_clickeado == "Imagen 1" and verificar_ingreso_datos(lista_banderas[1]):
            lista_banderas[1] = False
            respuestas = pregunta.obtener_dos_respuestas()
            recurso = [respuestas,"50-50"]
            
        elif comodin_clickeado == "Imagen 3" and verificar_ingreso_datos(lista_banderas[2]):
            lista_banderas[2] = False
            porcentajes = pregunta.crear_porcenajes(lista_porcentaje)
            recurso = [porcentajes,"Publico"]
            
    return recurso

def obtener_evento_videojuegos(pregunta:Pregunta, matriz_ganancia:list, mouse_posicion:tuple, cantidad_preguntas:int, ultima_ganancia:int) -> str: 
    """Obtener el evento de los videojuegos

    Args:
        pregunta (Pregunta): pregunta como objeto
        matriz_ganancia (list): matriz con las ganancias
        mouse_posicion (tuple): coordenadas del mouse
        cantidad_preguntas (int): cantidad de preguntas hasta el momento
        ultima_ganancia (int): ultima ganancia determinada

    Returns:
        str: "correcta" si la opcion clickeada es la correcta | "incorrecta" si la opcion clickeada es la incorrecta
    """
    lista_eventos = pygame.event.get()
    opcion_correcta = False
    for evento in lista_eventos:
        if evento.type == pygame.QUIT: # pregunto si presiono la X de la ventana
            pygame.quit()  
            sys.exit()     

        elif evento.type == pygame.MOUSEBUTTONDOWN :
            opcion_clickeada = pregunta.capturar_mouse_movimiento(mouse_posicion)
            
            if opcion_clickeada :
                if pregunta.es_correcta(opcion_clickeada):
                    opcion_correcta = "correcta"
                    pregunta.determinar_ganancia(matriz_ganancia, 10000,50000,273333, cantidad_preguntas, ultima_ganancia)
                else :  
                    opcion_correcta = "incorrecta"     
                
    return opcion_correcta        

