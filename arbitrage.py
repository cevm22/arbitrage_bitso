import threading
import datetime
import csv
import bitso
import time
import ccxt
import OB_Bitso

start_time = time.time()
print("----------------------")
print("---INICIANDO SCRIPT---")
print("----------------------")
erroresacumulados=0
def ex_bitso():
    try:
        api=bitso.Api()
        ob = api.order_book('btc_usd')
        #print(ob)
        #print(ob.updated_at)
        #print("Compra -> ",ob.bids[0].price) #ofertas a COMPRA
        #print("Volumen compra-> ",ob.bids[0].amount) #volumen de oferta
        #print("Venta -> ",ob.asks[0].price) #ofertas a VENTA
        #print("Volumen Venta-> ",ob.asks[0].amount) #volumen de oferta
        infoB=[float(ob.bids[0].price),float(ob.bids[0].amount),float(ob.asks[0].price),float(ob.asks[0].amount)]
        return(infoB)
    except Exception as e:
            f = open('ERRORfileBITSO.txt', 'w')
            f.write('HUBO UN ERROR bitso ->> - %s' % e)
            f.close()
            return ("error")



#def evaluar(Binfo,Pinfo):
def evaluar(tusd_btc, tusd_mxn,btc_mxn):
    compratusd_btc= tusd_btc[0]
    ventatusd_btc = tusd_btc[2]
    compratusd_mxn=tusd_mxn[0]
    ventatusd_mxn = tusd_mxn[2]
    comprabtc_mxn=btc_mxn[0]
    ventabtc_mxn=btc_mxn[2]
    capitalMXN = 1000.0
    capitalBTC = 0.01
    takerMXN=0.0065
    takerBTC=0.001
    vector=[]
    ###########
    #ecuacion MXN->BTC->USDT->MXN
    ###########
    a=capitalMXN/ventabtc_mxn
    a1=a-(a*takerMXN)
    a2=a1/compratusd_btc
    a3=a2-(a2*takerBTC)
    a4=a3*compratusd_mxn
    a5=a4-(a4*takerMXN)
    porcentajeA=((a5*100)/capitalMXN)-100
    ###########
    # ecuacion MXN->USDT->BTC->MXN
    ###########
    b=capitalMXN/ventatusd_mxn
    b1=b-(b*takerMXN)
    b2=b1*compratusd_btc
    b3=b2-(b2*takerBTC)
    b4=b3*comprabtc_mxn
    b5=b4-(b4*takerMXN)
    porcentajeB=((b5*100)/capitalMXN)-100
    ###########
    # ecuacion BTC->USDT->MXN->BTC
    ###########
    c=capitalBTC/compratusd_btc
    c1=c-(c*takerBTC)
    c2=c1*compratusd_mxn
    c3=c2-(c2*takerMXN)
    c4=c3/ventabtc_mxn
    c5=c4-(c4*takerMXN)
    porcentajeC=((c5*100)/capitalBTC)-100
    ###########
    # ecuacion BTC->MXN->USDT->BTC
    ###########
    d=capitalBTC*comprabtc_mxn
    d1=d-(d*takerMXN)
    d2=d1/ventatusd_mxn
    d3=d2-(d2*takerMXN)
    d4=d3*ventatusd_btc
    d5=d4-(d4*takerBTC)
    porcentajeD=((d5*100)/capitalBTC)-100

    vector.append([porcentajeA,porcentajeB,porcentajeC,porcentajeD])
    return(vector)


    #C_B= Binfo[0]
    #V_B= Binfo[2]
    #C_P = Pinfo[0]
    #V_P = Pinfo[2]
    #A=[]
    #if C_B >V_P:
        #print("SI hay BITSO")
        #porcentaje=  (1 - (V_P/C_B))*100
        #A.append(str(porcentaje))
    #else:
        #print("NO hay BITSO")
        #A.append(0)

    #if C_P>V_B:
        #print("SI hay POLONIEX")
        #porcentaje =  (1 - (V_B / C_P))*100
        #A.append(str(porcentaje))
    #else:
        #print("NO hay en POLONIEX")
        #A.append(0)
    #return(A)

def escribir():
    tusd_btc = OB_Bitso.bitso_orderbook('tusd_btc')
    tusd_mxn = OB_Bitso.bitso_orderbook('tusd_mxn')
    btc_mxn = OB_Bitso.bitso_orderbook('btc_mxn')
    #bitsoinfo=ex_bitso()
    #poloinfo=ex_poloniex()
    if tusd_btc == "error":
        print("Hubo un error", tusd_btc)
        time.sleep(5)
        return("error")
    if tusd_mxn == "error":
        print("Hubo un error", tusd_mxn)
        time.sleep(5)
        return("error")
    if btc_mxn == "error":
        print("Hubo un error", btc_mxn)
        time.sleep(5)
        return("error")
    # compra, vol, venta, vol
    #A=[% bitso, % polo] Valor return funcion "evaluar()"
    #print("%PORCENTAJE% ->  ",evaluar(bitsoinfo,poloinfo))
    #evaluacion=evaluar(bitsoinfo,poloinfo)
    #time-date	bitsoCOMPRA	volcompra	bitsoVENTA	volventa	poloCOMPRA	volcompra	poloVENTA	volventa	%BITSO	%POLONIEX
    tiempo = str(datetime.datetime.now())
    DATA=[]
    evaluacion=evaluar(tusd_btc,tusd_mxn,btc_mxn)
    #print(evaluacion)
    #DATA.append([tiempo, str(bitsoinfo[0]), str(bitsoinfo[1]), str(bitsoinfo[2]), str(bitsoinfo[3]), str(poloinfo[0]), str(poloinfo[1]), str(poloinfo[2]),
    #        str(poloinfo[3]), str(evaluacion[0]), str(evaluacion[1])])
    DATA.append([tiempo, str(tusd_btc[0]), str(tusd_btc[1]), str(tusd_btc[2]), str(tusd_btc[3]), str(tusd_mxn[0]), str(tusd_mxn[1]), str(tusd_mxn[2]), str(tusd_mxn[3]),str(btc_mxn[0]), str(btc_mxn[1]), str(btc_mxn[2]), str(btc_mxn[3]),
                 str(evaluacion[0][0]), str(evaluacion[0][1]),str(evaluacion[0][2]),str(evaluacion[0][3])])
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    with open("C:/Users/FIDGET1/Documents/drive/Scripts/BITSOarbitrajeDATA.csv", "a",newline='') as w:
        w = csv.writer(w)
        w.writerows(DATA)
    tiempo = datetime.datetime.now()
    print("Escrito -> ", tiempo)
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def run_check():
    errorscript=escribir()
    #bitsoinfo = ex_bitso()
    #errorscript = ex_bitso()
    #print(errorscript)
    if errorscript =="error":
        globals()["erroresacumulados"] = globals()["erroresacumulados"] +1
    errores=int(globals()["erroresacumulados"])

    if errores < 5:
        print("errores acumulados->",globals()["erroresacumulados"])
        threading.Timer(2.1, run_check).start()
    else:
        return



#escribir()
#run_check()
#bitsoinfo=ex_bitso()
#print(bitsoinfo)
#compra, vol, venta, vol
# A=[% bitso, % polo]
#print("%PORCENTAJE% ->  ",evaluar(bitsoinfo,poloinfo))
#print("--- %s seconds ---" % (time.time() - start_time))# TIEMPO DE EJECUCIÓN SCRIPT
