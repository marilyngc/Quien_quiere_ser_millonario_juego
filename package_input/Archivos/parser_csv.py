import re
def leer_archivos(path:str, lista):
    try:
        bandera_paso = False
        lista = [] #inicializo la lista
        with open(path, "r", encoding="utf-8") as archivo:
           
            for linea in archivo:
                if bandera_paso == False: #ignoro la primera linea
                    bandera_paso = True
                    continue
                registro = re.split(",|\n",linea)
                diccionario = {
                    "id": registro[0],
                    "pregunta": registro[1],
                    "comodin": registro[2],
                    "tipo": registro[3],
                }
               
                lista.append(diccionario)
        
        retorno =  lista
               
                
    except:
        retorno =  "A ocurrido un error al generar la lista en el archivo"  
    
    return retorno