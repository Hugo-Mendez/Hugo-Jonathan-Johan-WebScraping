import requests                     #Librería para abrir urls
import lxml.html as html            #Librería que permite trabajar con XPATH para realizar el web scraping
import threading                    #Librería que permite trabajar con hilos
from time import time               #Librería para trabajar con objetos time y poder calcular el tiempo de ejecución
import json                         #Librería que permite trabajar con archivos .json
import webbrowser                   #Librería que permite abrir un html
#Autores: Hugo Méndez, Jonathan Mendoza y Johan Zamora 

Links = [
    'https://store.playstation.com/es-cr/product/UP0700-CUSA05972_00-000000000TEKKEN7',#TEKKEN 7
    'https://store.playstation.com/es-cr/product/UP2113-CUSA06623_00-OUTLAST200000000',#Outlast 2
    'https://store.playstation.com/es-cr/product/UP0001-CUSA05904_00-FARCRY5GAME00000',#FAR CRY 5
    'https://store.playstation.com/es-cr/product/UP1003-CUSA12057_00-PRJMTN0000000000',#Fallout 76
    'https://store.playstation.com/es-cr/product/UP9000-PPSA01411_00-MARVELSSMMORALES',#Marvel's Spider-Man: Miles Morales
    'https://store.playstation.com/es-cr/product/UP9000-CUSA07408_00-00000000GODOFWAR',#God of War
    'https://store.playstation.com/es-cr/product/UP0006-CUSA19013_00-FIFAFOOTBALL2021',#FIFA 21
    'https://store.playstation.com/es-cr/product/UP1004-CUSA00419_00-GTAVDIGITALDOWNL',#GTA V
    'https://store.playstation.com/es-cr/product/UP0002-CUSA19035_00-CB4STANDARD00001',#Crash Bandicoot 4: It's About Time
    'https://store.playstation.com/es-cr/product/UP0006-CUSA08724_00-BATTLEFIELDV0000' #Battlefield V
    
]

LinksDix = [
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/tekken-7/?v=1d7b33fc26ca', # TEKKEN 7
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/outlast-2/?v=1d7b33fc26ca', # Outlast 2
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/far-cry-5/?v=1d7b33fc26ca', # Farcry 5
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/fallout-76/?v=1d7b33fc26ca', # Fallot 76
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/marvels-spider-man-miles-morales/?v=1d7b33fc26ca', # Marvel's Spider-Man: Miles Morales
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/god-of-war/?v=1d7b33fc26ca', # God of War
    'https://dixgamer.com/shop/juegos/ps4/deportes-ps4/fifa-21/?v=1d7b33fc26ca', # Fifa 21
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/gta-v/?v=1d7b33fc26ca', # GTA V
    'https://dixgamer.com/shop/juegos/ps4/aventura-ps4/crash-bandicoot-4-its-about-time/?v=1d7b33fc26ca', # Crash Bandicot
    'https://dixgamer.com/shop/juegos/ps4/accion-ps4/battlefield-5/?v=1d7b33fc26ca' # Battlefield V
]

Links_Ranks=[
    'https://www.3djuegos.com/8845/tekken-7/', # TEKKEN 7,
    'https://www.3djuegos.com/20634/outlast-2/',  # OUTLAST-2
    'https://www.3djuegos.com/29359/far-cry-5/',#FAR CRY 5  (BIEN)
    'https://www.3djuegos.com/32402/fallout-76/',#Fallout 76    (BIEN)
    'https://www.3djuegos.com/37593/spider-man-miles-morales/',#Marvel's Spider-Man: Miles Morales  (BIEN)
    'https://www.3djuegos.com/21016/god-of-war/', #God of War   (BIEN)
    'https://www.3djuegos.com/37068/fifa-21/', #FIFA 21     (BIEN)
    'https://www.3djuegos.com/19622/grand-theft-auto-v/', #GTA V    (BIEN)
    'https://www.3djuegos.com/37086/crash-bandicoot-4-its-about-time/', #Crash Bandicoot 4: It's About Time     (BIEN)
    'https://www.3djuegos.com/31536/battlefield-v/', #Battlefield V     (BIEN)
]

#Lista que contendrá la información de cada juego, almacenada en un diccionario individual
listaPlay=[{1: "", 2:[[], []], 3: "", 4: ""}, {1: "", 2:[[], []], 3: "", 4: ""}, {1: "", 2:[[], []], 3: "", 4: ""}, 
           {1: "", 2:[[], []], 3: "", 4: ""}, {1: "", 2:[[], []], 3: "", 4: ""}, {1: "", 2:[[], []], 3: "", 4: ""},
           {1: "", 2:[[], []], 3: "", 4: ""}, {1: "", 2:[[], []], 3: "", 4: ""}, {1: "", 2:[[], []], 3: "", 4: ""},
           {1: "", 2:[[], []], 3: "", 4: ""}
]

#Funcion Parse Game Rank
XPATH_GAME_RANK='//span[@class="pr t6"]/text()' #dejar[0] es voto de la pagina y [1]-Voto de usuario
XPATH_GAME_DURATION='//div[@class="vat w100_480 mar_l0_480 a_n"]/dl[position()=2]/dd[position()=3]/text()'

#Funcion Parse Game PlayStation
XPATH_PRICE_GAME = '//span[@class="psw-h3"]/text()'
XPATH_TITLE_GAME ='//h1[@class="psw-m-b-xs psw-h1 psw-l-line-break-word"]/text()'

#Funcion Parse Game Dixgamer
XPATH_TITLE_GAME2 = '//h1[@class="product-title product_title entry-title"]/text()'
XPATH_PRICE_GAME2 = '//span[@class="woocommerce-Price-amount amount"]/bdi/text()'


def parse_game_Rank(link, numero): #Función que recibe el enlace a un juego, luego realiza el web scraping con el fin de obtener el score y durabilidad de este (desde 3dJuegos)
    try:
        response = requests.get(link)
        if response.status_code == 200:
            game_title = response.content.decode('utf-8')  #Para que python lea bien y guarde caracteres como la ñ en archivos
            parsed = html.fromstring(game_title)  # toma el html de home y transformarlo para poder utilizarlo
            try:
                rank = parsed.xpath(XPATH_GAME_RANK)[0]
                duracion = parsed.xpath(XPATH_GAME_DURATION)[0]
                listaPlay[numero][3] = rank
                listaPlay[numero][4] = duracion
            except IndexError:  #EVITO que si alguna pagina no tiene price o description no se caiga la progra
                return
        else:
            raise ValueError(f'Error: {response.status_code}')  #Puede que el status sea 404
    except ValueError as ve:
        print(ve)


def parse_gamePlayStation(link, numero): #Función que recibe el enlace a un juego, luego realiza el web scraping con el fin de obtener el precio de este (desde PlayStation)
    try:
        response = requests.get(link)
        if response.status_code == 200:
            game_title = response.content.decode('utf-8')  #Para que python lea bien y guarde caracteres como la ñ en archivos
            parsed = html.fromstring(game_title)  # toma el html de home y transformarlo para poder utilizarlo
           
            try:
                title = parsed.xpath(XPATH_TITLE_GAME)[0]
                price = parsed.xpath(XPATH_PRICE_GAME)[0]
                price = price.replace("US$",'')
                price = price.replace(",",'.')
                price = float(price)
                listaPlay[numero][1] = title
                listaPlay[numero][2][0].append(price)
                listaPlay[numero][2][0].append("Play Station")
                return
                
            except IndexError:  #EVITO que si alguna pagina no tiene price o description no se caiga la progra
                return
        else:
            raise ValueError(f'Error: {response.status_code}')  #Puede que el status sea 404
    except ValueError as ve:
        print(ve)


def parse_game_dixgamer(link, numero): #Función que recibe el enlace a un juego, luego realiza el web scraping con el fin de obtener el precio de este (desde Dixgamer)
    try:
        response = requests.get(link)
        if response.status_code == 200:
            game_title = response.content.decode('utf-8')  #Para que python lea bien y guarde caracteres como la ñ en archivos
            parsed = html.fromstring(game_title)  # toma el html de home y transformarlo para poder utilizarlo
            try:
                price = parsed.xpath(XPATH_PRICE_GAME2)[2]
                price = price.replace("\xa0", '')
                price = price.replace(",",'.')
                price = float(price)
                listaPlay[numero][2][1].append(price)
                listaPlay[numero][2][1].append("Dixgamer")
                return
            except IndexError:  #EVITO que si alguna pagina no tiene price o description no se caiga la progra
                return
        else:
            raise ValueError(f'Error: {response.status_code}')  #Puede que el status sea 404
    except ValueError as ve:
        print(ve)


#-------------------------------------------------- Paralelismo --------------------------------------------------
def evaluacionURL(link, link2, numero): #Función que inicializa dos hilos distintos para obtener el precio mediante el web scraping
    #Se inicializan otros dos hilos (dentro de este hilo) cada uno obtiene el precio de una fuente distinta, esto de forma paralela
    t1 = threading.Thread(target = parse_gamePlayStation, args = (link, numero,)) #Se obtiene el precio desde la primera fuente
    t2 = threading.Thread(target = parse_game_dixgamer, args = (link2, numero,))  #Se obtiene el precio desde la segunda fuente
    t1.start() #Se inicializan los hilos(en este caso, estos se disparan dentro de otro hilo)
    t2.start()
    t1.join() #Instrucción que espera hasta que el hilo termine antes de ejecutar las siguientes instrucciones adicionales del programa (fuera de los hilos)
    t2.join()
    if listaPlay[numero][2][0][0] < listaPlay[numero][2][1][0]: #Condicional para eliminar el precio más alto
        listaPlay[numero][2].pop(1)
    else:
        listaPlay[numero][2].pop(0)
    return 
    

def getEvaluacionUrl(links, contador): #Función que recibe cierta cantidad de links y a cada uno de estos les obtiene el precio mediante la función evaluacionURL
    for x in links:
        evaluacionURL(x, LinksDix[contador], contador)
        contador += 1
    return 


def getRank(links, contador): #Función que recibe cierta cantidad de links y a cada uno de estos les obtiene el score y durabilidad mediante la función parse_game_Rank
    for i in links:
        parse_game_Rank(i, contador)
        contador += 1
    return


def paralel(): #Función que crea cuatro hilos distintos para realizar el web scraping y obtener la información necesaria de los juegos
    mitad = int(len(Links)/2) 
    subL1 = Links[0:mitad]          #Se crean 2 sublistas de la lista que contiene los links
    subL2 = Links[mitad:len(Links)]
    subRank1 = Links_Ranks[0:mitad] #Se crean 2 sublistas de la lista que contiene los links a la pagína desde la cual se obtiene el rank
    subRank2 = Links_Ranks[mitad:len(Links_Ranks)] 

    thread1 = threading.Thread(target = getEvaluacionUrl, args = (subL1, 0,)) #Primer hilo: obtiene el precio de la primera mitad de los juegos (subL1)
    thread2 = threading.Thread(target = getEvaluacionUrl, args = (subL2, 5,)) #Segundo hilo: obtiene el precio de la segunda mitad de los juegos (subL2)
    thread3 = threading.Thread(target = getRank, args = (subRank1, 0,)) #Tercer hilo: obtiene el rank y durabilidad de la primera mitad de los juegos (subRank1)
    thread4 = threading.Thread(target = getRank, args = (subRank2, 5,)) #Cuarto hilo: obtiene el rank y durabilidad de la segunda mitad de los juegos (subRank1)
    thread1.start()
    thread2.start()
    thread3.start()  #Se inicializan los hilos
    thread4.start()
    thread1.join()
    thread2.join()   #Instrucción que espera hasta que el hilo termine antes de ejecutar las siguientes instrucciones adicionales del programa (fuera de los hilos)
    thread3.join()
    thread4.join()
    return


def main(): #Función principal que invoca a la función paralel (la cual realiza el web scraping de forma paralela)
    t0 = time() #Objetos de tipo time, para imprimir el tiempo que tarda el método paralel
    paralel()
    t1 = time()
    print("Tiempo: {0:f} segundos".format(t1 - t0)) #Se imprime el tiempo

    with open("C:/ProyectoCompleto/Template/GamesData.json", "w") as games: # Se almacena toda la información de los juegos en un archivo.json
        games.write("var juegos = ")
        json.dump(listaPlay, games)
main()
webbrowser.open_new_tab("C:/ProyectoCompleto/Template/maquetacion-principal.html")


