# -*- coding: utf-8 -*-

import datetime
import time
import json
from django.http import HttpResponse
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


from btc_nextweek_okex.models import Trade as BtcTradeNextweek
from ltc_nextweek_okex.models import Trade as LtcTradeNextweek
from eth_nextweek_okex.models import Trade as EthTradeNextweek
from etc_nextweek_okex.models import Trade as EtcTradeNextweek
from xrp_nextweek_okex.models import Trade as XrpTradeNextweek
from eos_nextweek_okex.models import Trade as EosTradeNextweek
from trx_nextweek_okex.models import Trade as TrxTradeNextweek
from bch_nextweek_okex.models import Trade as BchTradeNextweek
from bsv_nextweek_okex.models import Trade as BsvTradeNextweek


from btc_quarter_okex.models import Trade as BtcTradeQuarter
from ltc_quarter_okex.models import Trade as LtcTradeQuarter
from eth_quarter_okex.models import Trade as EthTradeQuarter
from etc_quarter_okex.models import Trade as EtcTradeQuarter
from xrp_quarter_okex.models import Trade as XrpTradeQuarter
from eos_quarter_okex.models import Trade as EosTradeQuarter
from trx_quarter_okex.models import Trade as TrxTradeQuarter
from bch_quarter_okex.models import Trade as BchTradeQuarter
from bsv_quarter_okex.models import Trade as BsvTradeQuarter



def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret



def trades(request):
	reponse = ""
	if("btc_thisweek_okex" == request.GET["symbol"] or 
		"ltc_thisweek_okex" == request.GET["symbol"] or 
		"eth_thisweek_okex" == request.GET["symbol"] or 
		"etc_thisweek_okex" == request.GET["symbol"] or 
		"xrp_thisweek_okex" == request.GET["symbol"] or 
		"eos_thisweek_okex" == request.GET["symbol"] or 
		"trx_thisweek_okex" == request.GET["symbol"] or 
		"bch_thisweek_okex" == request.GET["symbol"] or 
		"bsv_thisweek_okex" == request.GET["symbol"]) :
		start_str = ""
		if(request.GET["start"] == "1200000000") :
			
			now = datetime.datetime.now()
			start = now - datetime.timedelta(hours=24*3, minutes=0, seconds=0)
			start_str = start.strftime("%Y-%m-%d %H:%M:%S")
		else:
			start = int(request.GET["start"])
			# start_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
			# start_str = datetime.datetime.fromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
			start_str = datetime.datetime.utcfromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
			
		if(start_str != ""):

			alltrade = []
			if("btc_thisweek_okex" == request.GET["symbol"]) :
				alltrade = BtcTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("ltc_thisweek_okex" == request.GET["symbol"]):
				alltrade = LtcTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("eth_thisweek_okex" == request.GET["symbol"]):
				alltrade = EthTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("etc_thisweek_okex" == request.GET["symbol"]):
				alltrade = EtcTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("xrp_thisweek_okex" == request.GET["symbol"]):
				alltrade = XrpTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("eos_thisweek_okex" == request.GET["symbol"]):
				alltrade = EosTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("trx_thisweek_okex" == request.GET["symbol"]):
				alltrade = TrxTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("bch_thisweek_okex" == request.GET["symbol"]):
				alltrade = BchTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]
			elif("bsv_thisweek_okex" == request.GET["symbol"]):
				alltrade = BsvTradeThisweek.objects.filter(timestamp__gte=get_aware_datetime(start_str))[:20000]


			for trade in alltrade:
				tradeTimestampStr = trade.timestamp.strftime('%Y-%m-%d %H:%M:%S') 
				tradeTimeArray = time.strptime(tradeTimestampStr, "%Y-%m-%d %H:%M:%S")
				tradeTime = int(time.mktime(tradeTimeArray))
				if("" == reponse) :
					reponse += str(tradeTime)+","+trade.price+","+trade.qty+","+trade.side
				else :
					reponse += "\n"+str(tradeTime)+","+trade.price+","+trade.qty+","+trade.side

	return HttpResponse(reponse)



