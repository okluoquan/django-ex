# -*- coding: UTF-8 -*-
VERSION = '0.7.1'



import time
import os
import urllib2
import socket
import json
import websocket
import ssl
import zlib
import threading
import requests

instrument_ids = ['futures/trade:EOS-USD-200327']


def buQiStr(content):
    content = str(content)
    right = 10 - len(content)
    while right>0:
        content = content + " "
        right = right - 1
    return content

def sendToIphoneThread(value1,value2,value3):
    t = threading.Thread(target=sendToIphone, args=(value1,value2,value3)) 
    t.start()

def sendToIphone(value1,value2,value3):
    sendTime = 0
    while sendTime<4:
        url = "https://maker.ifttt.com/trigger/eos/with/key/tAtTr4MbJ9-_d1WMg2Sk-"
        payload = {
            "value1": value1,
            "value2": value2,
            "value3": value3,
        }
        headers = {
            "Content-Type": "application/json"
        }
        resp = requests.post(url, data=json.dumps(payload), headers=headers)

        if resp.status_code!=200:
            sendTime = sendTime+1
        else:
            sendTime = 4


def sendPing(sock):
    while True:
        # print("ping")
        sock.send("ping")
        time.sleep(15)


def interest():
    CHARTS_HISTORY_URL = 'https://www.okex.me/api/futures/v3/instruments'
    HEADERS = {'User-Agent': 'pychartfeed/%s' % VERSION}
    instrument_id = 'EOS-USD-200327'
    preAmount = 0
    preTs = 0
    preMinutsAmount = 0
    urlerrorcount = 0

    while True:
        url = '%s/%s/open_interest' % (CHARTS_HISTORY_URL, instrument_id)
        req = urllib2.Request(url, None, HEADERS)
        try:
            chunkdata = urllib2.urlopen(req, None, timeout=15)
        except socket.timeout, err:
            print 'Timeout Error ' + str(type(err))
            urlerrorcount += 1
            time.sleep(1)
            continue
        except urllib2.URLError, err:
            print 'URLError = ' + str(err.reason)
            urlerrorcount += 1
            time.sleep(1)
            continue

        try:
            chunk = chunkdata.read()
        except urllib2.HTTPError, err:
            print 'HTTPError = ' + str(err.code)
            urlerrorcount += 1
            time.sleep(1)
            continue
        except urllib2.URLError, err:
            print 'URLError = ' + str(err.reason)
            urlerrorcount += 1
            time.sleep(1)
            continue
       

        result = json.loads(chunk)

        lastAmount = int(result["amount"])

        timeArray = ""
        if len(result["timestamp"])==20:
            timeArray = time.strptime(result["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        else:
            timeArray = time.strptime(result["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        ts = time.mktime(timeArray) + 3600 * 8
        otherTimeArray = time.localtime(ts)
        otherTime = time.strftime("%Y-%m-%d %H:%M:%S", otherTimeArray)
       
        if preTs!=0:
            if int(preTs/60) != int(ts/60):
                if lastAmount > preMinutsAmount:
                    print("                                                               \033[01;35m--------------    (%d     +%d)    ------------------\033[0m" % (lastAmount,(lastAmount-preMinutsAmount)))
                else:
                    print("                                                               \033[01;35m--------------    (%d     -%d)    ------------------\033[0m" % (lastAmount,abs((lastAmount-preMinutsAmount))))
                preMinutsAmount = lastAmount
        else:
            preMinutsAmount = lastAmount
            print"                                                               \033[01;35m--------------------------------------------------------\033[0m"

        preTs = ts 




        if preAmount != 0:
            if lastAmount>preAmount:
                if (lastAmount-preAmount)>20000:
                    print("                                                               \033[01;04;33m%s (%s)       %d     +%s GGGG\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr((lastAmount-preAmount))))
                    #playsound('./AlertSounds/3beeps.wav')
                    sendToIphoneThread(otherTime,"开",lastAmount-preAmount)
                elif (lastAmount-preAmount)>10000:
                    print("                                                               \033[01;04;33m%s (%s)       %d     +%s GGG\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr((lastAmount-preAmount))))
                    #playsound('./AlertSounds/3beeps.wav')
                    sendToIphoneThread(otherTime,"开",lastAmount-preAmount)
                elif (lastAmount-preAmount)>4000:
                    print("                                                               \033[01;04;33m%s (%s)       %d     +%s GG\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr((lastAmount-preAmount))))
                    #playsound('./AlertSounds/3beeps.wav')
                    sendToIphoneThread(otherTime,"开",lastAmount-preAmount)
                else:
                    print("                                                               \033[01;34m%s (%s)       %d     +%s XX\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr((lastAmount-preAmount))))
            
            if lastAmount<preAmount:
                if (preAmount-lastAmount)>20000:
                    print("                                                               \033[01;04;33m%s (%s)      %d     -%s GGGG\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr(abs((lastAmount-preAmount)))))
                    #playsound('./AlertSounds/belong.wav')
                    sendToIphoneThread(otherTime,"平",lastAmount-preAmount)
                elif (preAmount-lastAmount)>10000:
                    print("                                                               \033[01;04;33m%s (%s)      %d     -%s GGG\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr(abs((lastAmount-preAmount)))))
                    #playsound('./AlertSounds/belong.wav')
                    sendToIphoneThread(otherTime,"平",lastAmount-preAmount)
                elif (preAmount-lastAmount)>4000:
                    print("                                                               \033[01;04;33m%s (%s)       %d     -%s GG\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr(abs((lastAmount-preAmount)))))
                    #playsound('./AlertSounds/belong.wav')
                    sendToIphoneThread(otherTime,"平",lastAmount-preAmount)
                else:
                    print("                                                               \033[01;34m%s (%s)       %d     -%s XX\033[0m" % (result["timestamp"],otherTime,lastAmount,buQiStr(abs((lastAmount-preAmount)))))
            
            if lastAmount==preAmount:
                pass
                # print("%s (%s)                      %d  %d" % (result["timestamp"],otherTime,lastAmount,0))
        preAmount = lastAmount
        time.sleep(0.1)








def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated



def linesplit(sock):
    while True:
        try:
            r = sock.recv()
            r = inflate(r)
            if r == '':
                raise Exception('websocket failed')

        except Exception as sockerr:
            if str(sockerr) != 'timed out':  # Yes, there's not a better way...
                raise

        if("data" in r):
            r = json.loads(r)
            r = r["data"]
            for lineout in r :
                yield lineout



while True:

    try:
        s = websocket.create_connection("wss://149.129.81.70:10442/ws/v3",sslopt={"cert_reqs": ssl.CERT_NONE})

        t1 = threading.Thread(target=sendPing, args=(s ,)) 
        t1.start() 

        t2 = threading.Thread(target=interest) 
        t2.start() 

        sub_param = {"op": "subscribe", "args": instrument_ids}
        sub_str = json.dumps(sub_param)
        s.send(sub_str)
        accumulativeMount = 0
        accumulativeSide = ""
        accumulativePrice = 0
        accumulativeBegin = ""
        accumulativeBeginOther = ""
        accumulativeEnd = ""
        accumulativeEndOther = ""

        for result in linesplit(s):

            timeArray = ""
            if len(result["timestamp"])==20:
                timeArray = time.strptime(result["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            else:
                timeArray = time.strptime(result["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
            result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            ts = time.mktime(timeArray) + 3600 * 8
            otherTimeArray = time.localtime(ts)
            otherTime = time.strftime("%Y-%m-%d %H:%M:%S", otherTimeArray)

            
            


            if(result["side"] == "buy"):
                result["side"] = "buy "



            if accumulativeSide == "":
                accumulativeSide = result["side"]

                accumulativeBegin = result["timestamp"]
                accumulativeBeginOther = otherTime
                


            if accumulativeSide != result["side"]:
                accumulative = "{} ~ {}    {}  {}   {}".format(accumulativeBeginOther,accumulativeEndOther,accumulativeSide,round(accumulativePrice/accumulativeMount,2),accumulativeMount)
                if accumulativeMount > 4000:
                    sendToIphoneThread(accumulative,"","")
                    print("%s (%s) ~ %s (%s)    %s   %.2f    %d     TT" % (accumulativeBegin,accumulativeBeginOther,accumulativeEnd,accumulativeEndOther,accumulativeSide,accumulativePrice/accumulativeMount,accumulativeMount))
                
                accumulativeSide = result["side"]
                accumulativeMount = 0
                accumulativePrice = 0

                accumulativeBegin = result["timestamp"]
                accumulativeBeginOther = otherTime


            accumulativeMount = accumulativeMount + int(result["qty"])
            accumulativePrice = accumulativePrice + float(result["price"]) * int(result["qty"])
            
            accumulativeEnd = result["timestamp"]
            accumulativeEndOther = otherTime


            # if (int(result["qty"]))>=500:
            print("%s (%s)  %s  %s  %s" % (result["timestamp"],otherTime,result["side"],result["price"],result["qty"]))

            
          
    except KeyboardInterrupt:
        print "Ctrl+C detected..."
        break
    except Exception as e:
        print "%s, retrying..." % str(e)
        time.sleep(1)
        continue
    finally:
        print "Stopping streaming socket..."
        s.close()
        os._exit(0)

   