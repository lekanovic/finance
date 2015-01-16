# -*- coding: utf-8 -*-

import urllib, json
import ntplib
import socket
import time
from time import ctime


def getTime():
	while(1):
	    try:
		ntpClient = ntplib.NTPClient()
		response = ntpClient.request('3.us.pool.ntp.org')
		return ctime(response.tx_time)
	    except:
		pass

def collect_data():

    while(1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 7777))
        url = "http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json"
        response = urllib.urlopen(url);
        data = json.loads(response.read())
        goldPrice=0
        SEK=0
        for i in range(0, data['list']['meta']['count']):
            if data['list']['resources'][i]['resource']['fields']['name'] == "USD/SEK":
                SEK = data['list']['resources'][i]['resource']['fields']['price']
            if data['list']['resources'][i]['resource']['fields']['name'] == "GOLD 1 OZ":
                goldPrice = data['list']['resources'][i]['resource']['fields']['price']

        goldPrice = 1/float(goldPrice)
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        print ctime(response.tx_time)

        print "USD = %sSEK" % SEK
        print "Gold 1 once %s$" % (goldPrice)
        print "Gold 1 once %ssek" %((float(goldPrice)*float(SEK)))

        print "Gold 100g %s$" % (float(goldPrice)/31.1035*100 )
        print "Gold 100g %ssek" %((float(goldPrice)*float(SEK))/31.1035*100 )

        timestamp = getTime()
        gold_gram_usd = "%.3f" % (float(goldPrice)/31.1035*100)
        gold_gram_sek = "%.3f" % (float(goldPrice)*float(SEK)/31.1035*100)
        gold_ozt_sek = "%.3f" % (float(goldPrice)*float(SEK))
        gold_ozt_usd = "%.3f" % (goldPrice)

        data ="{\"timestamp\":\"%s\", \"USDSEK\":\"%s\", \"GoldOZTUSD\":\"%s\", \"GoldOZTSEK\":\"%s\",\"Gold100gSEK\":\"%s\",\"Gold100gUSD\":\"%s\"}" % (timestamp,SEK,gold_ozt_usd,gold_ozt_sek,gold_gram_sek,gold_gram_usd)
        print data
        client_socket.send(data)
        client_socket.close()
        time.sleep( 120 )


def main():
    collect_data()
if __name__ == "__main__":
    main()
