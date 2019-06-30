import websocket
import ssl
import zlib
import json
import time
import thread
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware


from btc_thisweek_okex.models import Trade as BtcTradeThisweek
from ltc_thisweek_okex.models import Trade as LtcTradeThisweek
from eth_thisweek_okex.models import Trade as EthTradeThisweek
from etc_thisweek_okex.models import Trade as EtcTradeThisweek
from xrp_thisweek_okex.models import Trade as XrpTradeThisweek
from eos_thisweek_okex.models import Trade as EosTradeThisweek
from trx_thisweek_okex.models import Trade as TrxTradeThisweek
from bch_thisweek_okex.models import Trade as BchTradeThisweek
from bsv_thisweek_okex.models import Trade as BsvTradeThisweek


# from btc_nextweek_okex.models import Trade as BtcTradeNextweek
# from ltc_nextweek_okex.models import Trade as LtcTradeNextweek
# from eth_nextweek_okex.models import Trade as EthTradeNextweek
# from etc_nextweek_okex.models import Trade as EtcTradeNextweek
# from xrp_nextweek_okex.models import Trade as XrpTradeNextweek
# from eos_nextweek_okex.models import Trade as EosTradeNextweek
# from trx_nextweek_okex.models import Trade as TrxTradeNextweek
# from bch_nextweek_okex.models import Trade as BchTradeNextweek
# from bsv_nextweek_okex.models import Trade as BsvTradeNextweek


# from btc_quarter_okex.models import Trade as BtcTradeQuarter
# from ltc_quarter_okex.models import Trade as LtcTradeQuarter
# from eth_quarter_okex.models import Trade as EthTradeQuarter
# from etc_quarter_okex.models import Trade as EtcTradeQuarter
# from xrp_quarter_okex.models import Trade as XrpTradeQuarter
# from eos_quarter_okex.models import Trade as EosTradeQuarter
# from trx_quarter_okex.models import Trade as TrxTradeQuarter
# from bch_quarter_okex.models import Trade as BchTradeQuarter
# from bsv_quarter_okex.models import Trade as BsvTradeQuarter


wsurl = "wss://149.129.81.70:10442/ws/v3"
instrument_ids = [
	"futures/trade:BTC-USD-190705",
	"futures/trade:LTC-USD-190705",
	"futures/trade:ETH-USD-190705",
	"futures/trade:ETC-USD-190705",
	"futures/trade:XRP-USD-190705",
	"futures/trade:EOS-USD-190705",
	"futures/trade:TRX-USD-190705",
	"futures/trade:BCH-USD-190705",
	"futures/trade:BSV-USD-190705",
]

modify_instrument_ids = False



def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret


def getInstrument_ids():
	if(len(instrument_ids) <= 0) :
		modify_instrument_ids = True 
	elif(not modify_instrument_ids) :
		modify_instrument_ids = True
	else:
		pass
	return modify_instrument_ids


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


def run(*args):

	disable_live = False

	while not disable_live:
		try:
			s = websocket.create_connection(wsurl,sslopt={"cert_reqs": ssl.CERT_NONE})
			sub_param = {"op": "subscribe", "args": instrument_ids}
			sub_str = json.dumps(sub_param)
			s.send(sub_str)


			for line in linesplit(s):

				# print(line)
			
				if("BTC-USD" in line['instrument_id']) :
					trade,created = BtcTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("LTC-USD" in line['instrument_id']):
					trade,created = LtcTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("ETH-USD" in line['instrument_id']):
					trade,created = EthTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("ETC-USD" in line['instrument_id']):
					trade,created = EtcTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("XRP-USD" in line['instrument_id']):
					trade,created = XrpTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("EOS-USD" in line['instrument_id']):
					trade,created = EosTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("TRX-USD" in line['instrument_id']):
					trade,created = TrxTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("BCH-USD" in line['instrument_id']):
					trade,created = BchTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				elif("BSV-USD" in line['instrument_id']):
					trade,created = BsvTradeThisweek.objects.get_or_create(instrument_id=line['instrument_id'], timestamp=get_aware_datetime(line['timestamp']), price=line['price'], qty=line['qty'], trade_id=line['trade_id'], side='b' if line['side'] == 'buy' else 's')
				
					trade.save()
				else:
					pass



		except KeyboardInterrupt:
			print "Ctrl+C detected..."
			break
		except Exception as e:
			print("aaaaaa")
			print "%s, retrying..." % str(e)
			time.sleep(1)
			continue
		finally:
			print("bbbbbb")
			print "Stopping streaming socket..."
			s.close()
    



def startWebsocket():
	thread.start_new_thread(run, ())

	


