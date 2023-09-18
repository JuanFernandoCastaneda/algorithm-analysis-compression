# Tarea 4: Compression

## Integrantes
- Juan Fernando - 201623311
- Juan Camilo Bonet - 202022466
- Laura Rodriguez - 201816069

## Instalación

Asegúrate de tener Python instalado en tu sistema. 

## Shannon-Fano

Este punto contiene el bono. Para usarlo solo es necesario correr la terminal interactiva y ponerle un nombre de archivo que esté guardado en la misma carpeta.

**(Modificación hecha a las 6:15 del 18 para completitud

A grandes rasgos, el programa agarra un archivo terminado en txt, lo lee y lo comprime en otro archivo con un texto mucho más corto. Esto se podrá comprobar en el archivo que termina con "_compression.txt". Lo anterior, pues hace uso de caracteres unicode, que se eligen por su codificación en bits. De esta forma, cada 8 bits de la codificación generada por el algoritmo de Shannon-Fano van a representar un caracter unicode. Además, y esto es lo importante de la compresión, guarda un archivo de códigos que termina en "_reverse_codes.json", donde por cada caracter DEL ALFABETO hay una entrada con su respectivo código asociado. Nos permitimos hacer uso de este archivo, pues va a tener complejidad espacial O(alfabeto), que será despreciable si el archivo de texto original es muy grande y el alfabeto no está en función de este (como suele pasar en la realidad). Se decidió este método en vez de un diccionario general para todos los lenguajes para no perder las especificidades (y por tanto optimizaciones) de cada lenguaje. Si mi lenguaje contiene solo consonantes, no debería por qué tener en cuenta que la "e" es la vocal más común en el inglés.  

Cuando se descomprime el archivo (con la opción 2), se va a imprimir a consola el resultado, pero al tiempo se guardará la descompresión en un archivo propio. Esto se podrá comprobar en el archivo que termina con "_decompressed.txt". Para caracteres muy raros, que no hagan parte de utf-8, la descompresión no funcionará bien. 

Dentro de la carpeta está un archivo (llamado prueba) donde se puede ver más o menos cuál será el resultado en cada paso.

)**

## Formato de Entrada
El archivo de entrada puede ser cualquier archivo de texto.
## Salida
El programa muestra a traves de la linea de comando la codificacion del texto, el número de bits esperado, la entropía en el peor de los casos y el número total de bits que se necesitarían para guardar el texto dado.
