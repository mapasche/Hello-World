from urllib import request

url = "https://www.instagram.com/"


resp = request.urlopen(url)

pre = request.urlretrieve(url)

print(dir(pre))


#dir(resp)  para saber funciones

print(dir(resp))


"""
print(resp.code) #200 es q todo esta bien
print(resp.length) #largo del contenido
print(resp.peek()) #nos entrega una parte de los q contiene

data = resp.read() #nos entrega lo q contiene
#solo se puede hace read una vez pq python termina la conexion
"""
    

#with open("pagina.txt", "wt") as file:
    # file.write(archivo.read().decode("utf-8")) 
