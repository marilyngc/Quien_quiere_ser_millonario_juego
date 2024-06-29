from .funciones import dibujar_titulo, get_font

BLANCO = (255, 255, 255)

class Pregunta: 
    def __init__(self, diccionario: dict) -> None:
        self.pregunta = diccionario["pregunta"]
        self.opciones_originales = diccionario["opciones"]
        self.opciones = diccionario["opciones"]
        self.correcta = diccionario["correcta"]
        self.dificultad = diccionario["dificultad"]
        self.posicion_x = 550
        self.posicion_y = 200  # posicion inicial
  
      
    def mostrar_preguntas(self,ventana): #PASAR A OTRA CLASE
        dibujar_titulo(ventana, self.pregunta, 10, BLANCO,None,(550,150))
                # Reiniciar la posición Y para las opciones
        self.posicion_y = 200
        # recorre las opciones
        for opciones in self.opciones:
            dibujar_titulo(ventana, opciones, 13, BLANCO, None,(self.posicion_x, self.posicion_y))

            self.posicion_y += 50
            
    
    def mouse_movimiento(self, mouse_posicion): #PASAR A OTRA CLASE
        retorno = None # Si no se clickeó ninguna opción, devuelve None
        self.posicion_y = 200
        for opcion in self.opciones:
            texto_renderizado = get_font(20).render(opcion, True, (255, 255, 255))
            texto_rect = texto_renderizado.get_rect(center=(self.posicion_x, self.posicion_y))
            
            if texto_rect.collidepoint(mouse_posicion):
                retorno = opcion # devuelve la opcion que clikeó
            self.posicion_y += 50   
                
        return retorno       
      
    def es_correcta(self,opcion) -> bool:
        retorno = False 
        if opcion == self.correcta:
            # print("repuesta correcta :D")
            retorno = True
        # else:
            # print("respuesta incorrecta :C")
            
        return retorno
    
    def determinar_ganancia(self, lista_ganancia:list[int], ganancia_facil:int, ganancia_media:int, ganancia_dificil:int) -> list:
     
        if self.dificultad == "facil":
            lista_ganancia.append(ganancia_facil)
        elif self.dificultad == "medio":
            lista_ganancia.append(ganancia_media)
        else:
            lista_ganancia.append(ganancia_dificil)
            
        return lista_ganancia
    
    def eliminar_dos_respuestas(self): #comodines
        #mejore
        i = 0
        contador = 0
        opciones_eliminadas = []
        #utilizo un while porque si elimino dentro de un for se rompe
        while i < len(self.opciones): # el valor "i" es el que se va a ir aumentando en cada iteracion
            if self.es_correcta(self.opciones[i]) == False and contador < 2:
                opciones_eliminadas.append(self.opciones.pop(i))
                contador += 1
                
            i +=1
        
        return opciones_eliminadas
    
    def crear_pista(self, lista_pista):
        
        for diccionario in lista_pista:
            if self.pregunta == diccionario["pregunta"]:
                print(diccionario["pista"])