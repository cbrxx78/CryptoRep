
# -*- coding: utf-8 -*-
import json
import requests
import time
import random
import microcule


def app(environ, start_response):
	# Imports the Google Cloud client library
	#from google.cloud import translate
	# predispongo una minitastiera, con il solo tasto Info
	keyboard_base = json.dumps({'keyboard': [["START","STOP"]],
								'one_time_keyboard': False,
								'resize_keyboard': True})
	
	
	# imposto il testo che da le info sul bot
	infoText="""  Ciao sono il bot * CryptoAlert * """
	# testo
	# imposto URL principali per inviare messaggi (quello per i messaggi e quello per le foto)
	URLT='https://api.telegram.org/bot' + Hook['env']['kkey'] + '/sendMessage'
	URLTF='https://api.telegram.org/bot' + Hook['env']['kkey'] + '/sendPhoto'

	# raccolgo nella variabile `testo` quello che gli utenti scriveranno in chat al bot
	#testoUser=Hook
	testo=Hook['params']['message']['text']
	# 
	if (testo=="Info" or testo=="/start"):
		richiesta=requests.get(URLT,verify=False,data={'chat_id':Hook['params']['message']['chat']['id'],
				'text':infoText,'parse_mode':'Markdown','reply_markup':keyboard_base})
		
		json_data=json.loads(richiesta.text)
		sendURL ='https://api.telegram.org/bot' + Hook['env']['kkey'] + '/sendMessage'
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		requests.post(sendURL, data=json.dumps(json_data), headers=headers, verify=False)
		start_response('200 OK', [('content-type', 'text/plain')])
		return '\n'
	# 
	# URL per interrogare le API della NASA, usando le keyword inserite dall'utente
	#URL="https://images-api.nasa.gov/search?media_type=image&q="+testo
	URL_BTC="https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR"
	URL_ETH="https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=EUR"
	URL_LTC="https://api.coinmarketcap.com/v1/ticker/litecoin/?convert=EUR"
	URL_BCH="https://api.coinmarketcap.com/v1/ticker/bitcoin-cash/?convert=EUR"
    # se l'utente chiede info con il tasto Info o se si iscrive con `/start` avrà inviato le info sul bot
	if (testo=="START"):
		
		while True:	
			if (testo=="STOP"):
				break
			
			richiesta=requests.get(URLT,verify=False,data={'chat_id':Hook['params']['message']['chat']['id'],
				'text':infoText,'parse_mode':'Markdown','reply_markup':keyboard_base})
			
			for n in range(1, 5):
				req=""
				
				if(n==1):
					req=URL_BTC		
				elif (n==2):
					req=URL_ETH
				elif (n==3):
					req=URL_BCH
				elif (n==4):
					req=URL_LTC
					
				r = requests.get(req, verify=False)
				json_data=json.loads(r.text)
				
				id=json_data[0]['id']
				
				name=json_data[0]["name"]
				price = json_data[0]["price_eur"]
				
				data={'chat_id':Hook['params']['message']['chat']['id'],'text':name + ' = ' + price,'parse_mode':'Markdown','reply_markup':keyboard_base}
				richiesta=requests.get(URLT,verify=False,data=data)
			
			time.sleep(5)
				
		
	# altrimenti il bot inizierà a elaborare quello che l'utente ha scritto
		
	json_data=json.loads(richiesta.text)
	sendURL ='https://api.telegram.org/bot' + Hook['env']['kkey'] + '/sendMessage'
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	requests.post(sendURL, data=json.dumps(json_data), headers=headers, verify=False)
	start_response('200 OK', [('content-type', 'text/plain')])
	return '\n'
		
if __name__ == '__main__':
    microcule.wsgi(Hook).run(app)		
				
		
