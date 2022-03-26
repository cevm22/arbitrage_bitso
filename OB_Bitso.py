#Script consultas Order Book BITSO
import datetime
import bitso
import time
import ccxt
import requests
from  credenciales import*

llave=bitsokeys()

def bitso_orderbook(par):
    #BITSO
    #print("BITSO")
    try:
        api=bitso.Api()
        ob = api.order_book(par)
        #print(ob)
        #print(ob.updated_at)
        #print("---------------")
        #print(par)
        #print("Compra -> ",ob.bids[0].price) #ofertas a COMPRA
        #print("Volumen compra-> ",ob.bids[0].amount) #volumen de oferta
        #print("Venta -> ",ob.asks[0].price) #ofertas a VENTA
        #print("Volumen Venta-> ",ob.asks[0].amount) #volumen de oferta
        #print("---------------")
        infoB=[float(ob.bids[0].price),float(ob.bids[0].amount),float(ob.asks[0].price),float(ob.asks[0].amount)]
        return(infoB)
    except Exception as e:
            f = open('ERRORfileBITSO.txt', 'w')
            f.write('HUBO UN ERROR bitso ->> - %s' % e)
            f.close()
            return ("error")
    #BITSO
    ###############

def wallet():
    try:
        api=bitso.Api(llave[0],llave[1])
        balances=api.balances()
        # BTC, XRP, USD, MXN
        btc=balances.btc.available
        xrp=balances.xrp.available
        usd=balances.usd.available
        mxn=balances.mxn.available
        capitales=[btc,xrp,usd,mxn]
        return(capitales)

    except Exception as e:
        f = open('ERROR-balances.txt', 'w')
        f.write('HUBO UN ERROR bitso ->> - %s' % e)
        f.close()

    return

def makeatrade(book,side,order_type,major_minor,amount):
    #book = 'xrp_usd'
    #side= 'buy' or 'sell'
    #order_type= 'limit' or 'market'
    #major_minor= 'major' or  'menor' (#“Major_Minor”. For example: “btc_mxn”)
    #cantidad=str(amount)

    try:
        api=bitso.Api(llave[0],llave[1])
        #capital=wallet() #[btc,xrp,usd,mxn]
        #books 'xrp_usd' 'btc_usd' 'xrp_btc'
        #order = api.place_order(book='btc_mxn', side='buy', order_type='limit', major='.01', price='7000.00')
        if major_minor=='major':
            order = api.place_order(book=book,side=side,order_type=order_type,major=str(amount))
            #order='major'
            return(order)
        if major_minor=='minor':
            order = api.place_order(book=book, side=side, order_type=order_type, minor=str(amount))
            #order = 'minor'
            return (order)
        print("orden enviada")

    except Exception as e:
        f = open('ERROR-makingatrade-.txt', 'w')
        f.write('HUBO UN ERROR bitso ->> - %s' % e)
        f.close()
        print("error en mandar orden de trade")
    return


#books 'xrp_usd' 'btc_usd' 'xrp_btc'
#book = 'xrp_usd'
    #side= 'buy' or 'sell'
    #order_type= 'limit' or 'market'
    #major_minor= 'major' or  'menor' (#“Major_Minor”. For example: “btc_mxn”)
    #cantidad=str(amount)
#a=Mmakeatrade('xrp_btc','buy','market','major','18')
#print(a)
#print(wallet())


def telebot(bot_message):
    bot_token = TOKEN_ID
    bot_chatID = CHAT_TELEGRAM_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()



