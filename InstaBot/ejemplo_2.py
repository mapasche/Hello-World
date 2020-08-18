from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = "C:\\Users\\Martin Pasche\\Desktop\\Hello-World\\InstaBot\\chromedriver.exe"
link = "https://www.instagram.com"
username = "martin.pasche@hotmail.com"
password = "sugarglider0680"

cantidad_seguidores_minimo = 1000
lugar = ["chile", "cl", "santiago"]

usuarios_revisados_seguidores = []
usuarios_revisados_sorteo = []

posibles_influencers = {}



def navegar_usuario_principal():
    try:
        #hace click en mi icono de usuario
        imagen_element = web.find_element_by_xpath("//div[@class='Fifk5'][5]")
        imagen_element.click()
        time.sleep(0.5)

        #hace click en el boton perfil
        perfil_element = web.find_element_by_xpath("//div[@class='Fifk5'][5]/div[2]/div[1]/div[2]/div[2]/a[1]")
        perfil_element.click()
        #nombre usuario mio
        nombre_usuario = web.find_element_by_xpath("//div[@class='nZSzR']/h2[1]")
        añadir_usuario_revisado_seguidores(nombre_usuario.text)


        seguidores_elementos = web.find_element_by_xpath("//section[@class='zwlfE']/ul[1]/li[2]/a[1]/span")
        cantidad_seg = int(seguidores_elementos.text)
        print(nombre_usuario.text, cantidad_seg)

        #abre la pestaña de gente seguida
        seguidos_element = web.find_element_by_xpath("//section[@class='zwlfE']/ul[1]/li[3]")
        seguidos_element.click()
    
    except Exception as e:
        print("Navegar usuario principal", e)
        web.close()

    else:
        algoritmo_busqueda()


def algoritmo_busqueda ():
    
    try:
       
        #transformar princiapl al primero de sus segujires y asi sucesivamente
    
        seguidos_element = web.find_element_by_xpath("//section[@class='zwlfE']/ul[1]/li[3]/a[1]/span")
        try:
            num_seguidos = int(seguidos_element.text)
        except Exception as e:
            print(e)
            num_seguidos = 0 #-------------------------------------------------------------


        for num in range(1, num_seguidos + 1):
            
            wait = WebDriverWait(web, 5)
            dialog_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div._1XyCr')))




            #dialog_scroll_element = dialog_element.find_element_by_xpath("//div[@class='isgrP']/ul[1]")

            entrar = False
            while not entrar:
                try:
                    dialog_user_element = dialog_element.find_element_by_xpath(f"//div[@class='PZuss']/li[{num}]/div[1]/div[1]/div[2]")
                    dialog_user_element.click()

                except (exceptions.NoSuchElementException, 
                    exceptions.StaleElementReferenceException, 
                    exceptions.ElementNotInteractableException) as e:

                    print(e)
                    dialog_user_elements = dialog_element.find_elements_by_xpath("//div[2]/ul[1]/div[1]/li")
                    last_element = dialog_element.find_element_by_xpath(f"//div[@class='PZuss']/li[{len(dialog_user_elements)}]")
                    print(dialog_user_elements)
                    web.execute_script("arguments[0].scrollIntoView(true);", last_element)

                else:
                    entrar = True

            username = obtener_nombre()

            if username not in usuarios_revisados_seguidores:
                añadir_usuario_revisado_seguidores(username)
                
                cantidad_seg = obtener_seguidores()
                
                if cumple_requisitos(cantidad_seg):
                    añadir_influencer(username, cantidad_seg)

            web.back()


        
            



            #revisar seguidores cuenta principal

        


    except KeyboardInterrupt:
        print("cerrando el programa")
        print(posibles_influencers)
        print("\n")
        print("Usuarios revisados : ", usuarios_revisados_seguidores)

    except exceptions.NoSuchElementException as e:
        print(e)

    """
    finally:
        try:
            web.close()
        except Exception:
            print("Error q no se pq ocurre")
    """
    
    



def obtener_nombre():
    username_element = web.find_element_by_xpath("//div[@class='nZSzR']/h2[1]")
    return username_element.text
    

def obtener_seguidores():
    wait = WebDriverWait(web, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//section[@class='zwlfE']/ul[1]/li[2]/a[1]/span" )))
    num =  element.text
    if 'm' in num:
        num = num[:-1]
        num = float(num)
        num *= 1000000
    elif 'k' in num:
        num = num[:-1]
        num = float(num)
        num *= 1000

    elif ',' in num:
        num = num.replace(",", "")
    
    num = int(num)
    return num

def obtener_localizacion():
    pass

def añadir_influencer(nombre, seguidores):
    nombre = str(nombre)
    nombre = nombre.strip()
    if nombre not in posibles_influencers:
        posibles_influencers[nombre] = seguidores

def añadir_usuario_revisado_seguidores (nombre):
    nombre = str(nombre)
    nombre = nombre.strip()
    if nombre not in usuarios_revisados_seguidores:
        usuarios_revisados_seguidores.append(nombre)

def añadir_usuario_revisado_sorteo(nombre):
    nombre = str(nombre)
    nombre = nombre.strip()
    if nombre not in usuarios_revisados_sorteo:
        usuarios_revisados_sorteo.append(nombre)

def cumple_requisitos(cantidad_seg):
    cantidad_seg = int(cantidad_seg)
    if cantidad_seg > cantidad_seguidores_minimo:
        return True
    else:
        return False







if __name__ == "__main__":

    web = webdriver.Chrome(driver)
    web.implicitly_wait(10)
    web.get(link)
    try:
        element_username = web.find_element_by_name("username")
        element_username.send_keys(username)
        element_password = web.find_element_by_name("password")
        element_password.send_keys(password)
        element_password.submit()
        
    except Exception as e:
        print("Error inicial", e)
        web.quit()
    else:
        navegar_usuario_principal()






