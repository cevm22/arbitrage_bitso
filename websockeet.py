import websocket, json
import time
import datetime
import csv
import bitso
from OB_Bitso import *

xrp_usd_lastbids=[]
xrp_usd_lastasks=[]
btc_usd_lastbids=[]
btc_usd_lastasks=[]
xrp_btc_lastbids=[]
xrp_btc_lastasks=[]
saldoactual=[]
capitalXRP=10.0
taker=0.001

def imprimir():
    #print("VECTOR BIDS->",globals()['xrp_usd_lastbids'])
    #print("VECTOR ASKS->",globals()['xrp_usd_lastasks'])
    print("funcion imprimir")
    time.sleep(2)
    print("volver a iniciar funcion")
    time.sleep(1)
    imprimir()


def valores():
    compraxrp_usd = globals()['xrp_usd_lastbids'][0][0]['r']
    ventaxrp_usd = globals()['xrp_usd_lastasks'][0][0]['r']
    comprabtc_usd = globals()['btc_usd_lastbids'][0][0]['r']
    ventabtc_usd = globals()['btc_usd_lastasks'][0][0]['r']
    compraxrp_btc = globals()['xrp_btc_lastbids'][0][0]['r']
    ventaxrp_btc = globals()['xrp_btc_lastasks'][0][0]['r']
    vector=[]
    vector.append([float(compraxrp_usd),float(ventaxrp_usd),float(comprabtc_usd),float(ventabtc_usd),float(compraxrp_btc),float(ventaxrp_btc)])
    return vector

def escribir(porcentaje):
    porcentajeganancia=str(porcentaje)
    vector=valores()
    compraxrp_usd = str(vector[0][0])
    vol1=str(float(globals()['xrp_usd_lastbids'][0][0]['a'])+float(globals()['xrp_usd_lastbids'][0][1]['a'])+float(globals()['xrp_usd_lastbids'][0][2]['a']))
    ventaxrp_usd = str(vector[0][1])
    #vol2=str(globals()['xrp_usd_lastasks'][0][0]['a'])
    vol2 = str(
        float(globals()['xrp_usd_lastasks'][0][0]['a']) + float(globals()['xrp_usd_lastasks'][0][1]['a']) + float(
            globals()['xrp_usd_lastasks'][0][2]['a']))
    comprabtc_usd = str(vector[0][2])
    #vol3=str(globals()['btc_usd_lastbids'][0][0]['a'])
    vol3 = str(
        float(globals()['btc_usd_lastbids'][0][0]['a']) + float(globals()['btc_usd_lastbids'][0][1]['a']) + float(
            globals()['btc_usd_lastbids'][0][2]['a']))
    ventabtc_usd = str(vector[0][3])
    #vol4=str(globals()['btc_usd_lastasks'][0][0]['a'])
    vol4 = str(
        float(globals()['btc_usd_lastasks'][0][0]['a']) + float(globals()['btc_usd_lastasks'][0][1]['a']) + float(
            globals()['btc_usd_lastasks'][0][2]['a']))

    compraxrp_btc = str(vector[0][4])
    #vol5=str(globals()['xrp_btc_lastbids'][0][0]['a'])
    vol5 = str(
        float(globals()['xrp_btc_lastbids'][0][0]['a']) + float(globals()['xrp_btc_lastbids'][0][1]['a']) + float(
            globals()['xrp_btc_lastbids'][0][2]['a']))
    ventaxrp_btc = str(vector[0][5])
    #vol6=str(globals()['xrp_btc_lastasks'][0][0]['a'])
    vol6 = str(
        float(globals()['xrp_btc_lastasks'][0][0]['a']) + float(globals()['xrp_btc_lastasks'][0][1]['a']) + float(
            globals()['xrp_btc_lastasks'][0][2]['a']))
    DATA=[]
    tiempo = str(datetime.datetime.now())
    DATA.append([tiempo,compraxrp_usd,vol1,ventaxrp_usd,vol2,comprabtc_usd,vol3,ventabtc_usd,vol4,compraxrp_btc,vol5,ventaxrp_btc,vol6,porcentajeganancia])

    with open("F:/Drive/trading stuff/Scripts/WebSocket-aribtrage.csv", "a", newline='') as w:
        w = csv.writer(w)
        w.writerows(DATA)
    print("Escrito -> ", tiempo)


def calculo():
        vector=valores()
        compraxrp_usd=vector[0][0]
        ventaxrp_usd=vector[0][1]
        comprabtc_usd=vector[0][2]
        ventabtc_usd=vector[0][3]
        compraxrp_btc=vector[0][4]
        ventaxrp_btc=vector[0][5]
        capital=float(globals()['capitalXRP'])
        ###########
        # ecuacion XRP->USD->BTC->XRP
        ###########
        a=capital*compraxrp_usd# compro USD
        a1=a-(a*taker)
        a2=a1/ventabtc_usd #compro BTC
        a3=a2-(a2*taker)
        a4=a3/ventaxrp_btc #compro XRP
        a5=a4-(a4*taker)
        a6=((a5*100)/capital)-100
        porcentaje=a6
        tiempo = str(datetime.datetime.now())
        print("ULTIMA CONSULTA -->", tiempo)
        print("% arbitraje -> ",porcentaje)
        #print("a3 BTc-> ",a3)
        #print("a5 XRP-> ", a5)
        #pruebaarbitraje(str(round(capitalXRP,8)), str(round(float(a2 * 1.001),8)), str(round(float(a4 * 1.001),8)),str(porcentaje),str(a))
        if porcentaje >= 0.1:
            tiempo = str(datetime.datetime.now())
            pruebaarbitraje(str(round(capitalXRP,8)), str(round(float(a1 * 1.0),8)), str(round(float(a5 * 1.0),8)),str(porcentaje),str(a))
            escribir(porcentaje)
            vectorcalculos = []
            vectorcalculos.append([a1, a2, a3, a4, a5, a6])
            resultadoscalculo(vectorcalculos)
            print("OPORTUNIDAD ESCRITA -->", tiempo)

            return

def resultadoscalculo(vectorcalculos):
    vec=vectorcalculos
    print(vec)
    header=str("=====CALCULOS=====")
    telebot(header)

    mensaje = str("a1 --> " + str(vec[0][0]) + "\n a2--> " + str(vec[0][1]) + "\n a3--> " + str(vec[0][2]) + "\n a4--> " + str(vec[0][3]) +
                  "\n a5--> " + str(vec[0][4]) + "\n a6--> " + str(vec[0][5]))
    telebot(mensaje)

    footer = str("=====CALCULOS=====")
    telebot(footer)
    time.sleep(2)
    cerrar(ws)

def escribirprueba(vector):
    with open("F:/Drive/trading stuff/Scripts/PRIMERAPRUEBATRADING.csv", "a", newline='') as w:
        w = csv.writer(w)
        w.writerows(vector)
    print("escribiendo la prueba")
    return


def pruebaarbitraje(capital,btc,xrp,porcentaje,usd):
    try:

        formatobtc=float(btc)
        formato = "{p:.8f}"
        btc1=(formato.format(p=formatobtc))
        #print("====wallet====")
        #BTC, XRP, USD, MXN
        #saldos = wallet()
        # books 'xrp_usd' 'btc_usd' 'xrp_btc'

        #====VENDER XRP por USD====
        TRADE1=makeatrade('xrp_usd', 'sell', 'market', 'major', str(capital))
        #====COMPRAR BTC por USD====
        TRADE2=makeatrade('btc_usd', 'buy', 'market', 'minor', str(btc1)) #ultimo cambio
        #====COMPRAR XRP por BTC====
        TRADE3=makeatrade('xrp_btc', 'buy', 'market', 'major', str(xrp))

        time.sleep(5)
        vector = []
        vector.append([capital, usd, btc1, xrp, porcentaje])
        # BTC, XRP, USD, MXN
        saldos= globals()['saldoactual']
        saldobtc = str(saldos[0])
        saldoxrp = str(saldos[1])
        saldousd = str(saldos[2])
        mensajesaldos = str("BTC-> " + saldobtc + '\n' + 'XRP-> ' + saldoxrp + '\n' + 'USD-> ' + saldousd)
        print("cerrando programa")
        #print(capital, btc, xrp)
        telebot("=====================================")
        header= str("INFO WALLET ANTES DEL ARBITRAJE")
        telebot(header)
        telebot(mensajesaldos)
        header2= str("TRADES DE ARBITRAJE")
        telebot(header2)
        mensaje= str("inversion XRP ->" + capital + "\n BTCUSD--> " +btc1+ "\nXRP--->" +xrp)
        telebot(mensaje)
        time.sleep(5)
        header3 = str("NUEVOS SALDOS EN WALLET")
        telebot(header3)
        nuevo = wallet()
        nuevobtc = str(nuevo[0])
        nuevoxrp = str(nuevo[1])
        nuevousd = str(nuevo[2])
        nuevossaldos = str("BTC-> " + nuevobtc + '\n' + 'XRP-> ' + nuevoxrp + '\n' + 'USD-> ' + nuevousd)
        telebot(nuevossaldos)

        escribirprueba(vector)
        trade = []
        trade.append([TRADE1, TRADE2, TRADE3])
        escribirprueba(trade)
        globals()['saldoactual'] = wallet()
        globals()['xrp_btc_lastbids'] = []
        globals()['xrp_btc_lastasks'] = []
        globals()['btc_usd_lastbids'] = []
        globals()['btc_usd_lastasks'] = []
        globals()['xrp_usd_lastbids'] = []
        globals()['xrp_usd_lastasks'] = []
        return()#cerrar(ws)

    except Exception as e:
        f = open('ERROR-DEFpruebaarbitraje-.txt', 'w')
        f.write('HUBO UN ERROR bitso ->> - %s' % e)
        f.close()
        print("error en mandar orden de trade")
    return


def on_open(ws):
    print("OPENED")
    auth_data={ "action": "subscribe",
                "book": "xrp_usd",
                "type": "orders"
    }
    auth_data2 = {"action": "subscribe",
                 "book": "xrp_btc",
                 "type": "orders"
                 }
    auth_data3 = {"action": "subscribe",
                  "book": "btc_usd",
                  "type": "orders"
                  }
    ws.send(json.dumps(auth_data))
    ws.send(json.dumps(auth_data2))
    ws.send(json.dumps(auth_data3))

def on_message(ws,message):
    #print("=====MENSAJE RECIBIDO=====")
    mensaje=json.loads(message) #cargar el mensaje del servidor en JSON
    book=mensaje['book']
    payload = mensaje['payload']  # obtener el Payload del orderbook
    if book=="xrp_usd":
        #print("=====XRP_USD=====")
        asks = payload['asks']
        bids = payload['bids']
        globals()['xrp_usd_lastbids']=[[bids[0], bids[1], bids[2]]]
        globals()['xrp_usd_lastasks']=[[asks[0], asks[1], asks[2]]]
        #imprimir()
        calculo()

    if book=="btc_usd":
        #print("=====BTC_USD=====")
        asks = payload['asks']
        bids = payload['bids']
        globals()['btc_usd_lastbids']=[[bids[0], bids[1], bids[2]]]
        globals()['btc_usd_lastasks']=[[asks[0], asks[1], asks[2]]]
        calculo()
        #print(payload)
    if book=="xrp_btc":
        #print("=====XRP_BTC=====")
        asks = payload['asks']
        bids = payload['bids']
        globals()['xrp_btc_lastbids']=[[bids[0], bids[1], bids[2]]]
        globals()['xrp_btc_lastasks']=[[asks[0], asks[1], asks[2]]]
        calculo()
        #print(payload)

    #bids=payload['bids'] #compra
    #asks = payload['asks'] #venta
    #print(payload)
    #Print("===BIDS==",bids)
    #print("=========")
    #print("==ASKS==",asks)
    #print("=========")
    #print(bids[0]) # precio de compra más alto
    #print(asks[0]) #precio de venta más bajo
def on_close(ws):
    try:
        f = open('CIERRE CANAL.txt', 'w')
        f.write('HUBO UN ERROR bitso TRY->> ')
        f.close()
        mensaje="INGRESANDO AL TRY DE ->ONCLOSE"
        print(mensaje)
        telebot(mensaje)
        mensaje3 = "RESTAURANDO CANAL"
        telebot(mensaje3)
        time.sleep(30)
        reiniciar()


    except Exception as e:
        f = open('CIERRE CANAL.txt', 'w')
        f.write('HUBO UN ERROR bitso EXCEPT->>     %s' % e)
        f.close()
        mensaje2="ERROR EN COMUNICACION, FALTA DE MENSAJE"
        print(mensaje2)
        telebot(mensaje2)
        mensaje4 = "RESTAURANDO CANAL"
        telebot(mensaje4)
        time.sleep(30)
        reiniciar()

def cerrar(ws):
    ws.close()
def reiniciar():
    mensaje = "REINICIANDO"
    telebot(mensaje)
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()


socket= 'wss://ws.bitso.com'
globals()['saldoactual']=wallet()
print(globals()['saldoactual'])
##ws=websocket.WebSocketApp(socket,on_open=on_open, on_message=on_message,on_close=on_close,)
##ws.run_forever()


