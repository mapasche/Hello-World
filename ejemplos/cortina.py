string_cantidad_disparos = input() #lee la primera linea del input

print(string_cantidad_disparos) #con esto sabremos q tipo de variable es

cantidad_disparos = int(string_cantidad_disparos) #transformamos a int el input

codigo_hit = "Hit!" #esta será nuestra referencia para saber si achuntamos o no

cantidad_achuntados = 0 #nuestro contador de golpes efectivos

for i in range(cantidad_disparos): 
    #Hacemos un buclee para la cantidad de veces q se dispara
    #o para la cantidad de veces que se nos entregara el input

    linea = input() #leemos la siguiente linea
    print(linea) #para saber q contiene la linea

    if linea == codigo_hit: #si el input de disparo es igual a "Hit!"
        #si es verdadero, le achuntó, por lo que sumamos al contador

        cantidad_achuntados += 1

    #si linea no es "Hint!, hacemos nada"


    #repetimos el buclee hasta q se acaben los input


#imprimimos la cantida de hits
print(cantidad_achuntados)

