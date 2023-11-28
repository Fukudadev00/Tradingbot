from web3 import Web3
import json
import time

BSC_url = 'https://bsc-dataseed.binance.org/'
Auro_url = 'https://aurora-mainnet.infura.io/v3/4596197da90f45b4b7a4e8c8db1b9acb'
Poly_url = 'https://polygon-rpc.com'
tradeamount = int(input("Input your trading USDC amount: "))

f = open('router_abi.json')
router_abi = json.load(f)
f.close()

def getPrice(addr, url, path, amount, decimal):
    web3 = Web3(Web3.HTTPProvider(url))
    router_contract = web3.eth.contract(address= addr,abi = router_abi)
    price = router_contract.functions.getAmountsOut((10**decimal[0]*amount), path).call()
    price[0] = float(price[1]/(10**decimal[1]))
    path.reverse()
    price1 = router_contract.functions.getAmountsIn((10**decimal[0]*amount),path).call()
    price[1] = float(price1[0]/(10**decimal[1]))
    return price

def price():
    while(1):
        bscprice = getPrice('0x10ED43C718714eb63d5aA57B78B54704E256024E', BSC_url, path=["0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56", "0x68784ffaa6Ff05E3e04575DF77960DC1D9F42b4a"], amount = tradeamount, decimal=[18,18])
        polyprice = getPrice('0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607', Poly_url, path=['0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174','0x04429fbb948BBD09327763214b45e505A5293346'], amount = tradeamount, decimal=[6, 18])
        auroprice = getPrice('0x2CB45Edb4517d5947aFdE3BEAbF95A582506858B', Auro_url, path=['0xB12BFcA5A55806AaF64E99521918A4bf0fC40802','0x2BAe00C8BC1868a5F7a216E881Bae9e662630111'], amount = tradeamount,  decimal=[6,18])  
        print('BSC price: ', bscprice)
        print('Polygon price: ', polyprice)
        print('Aurora price: ',auroprice)
        if bscprice[0] > auroprice[0] and bscprice[0] > polyprice[0]:
            if auroprice[1]<polyprice[1]:
                eprofit = (bscprice[0] - auroprice[1])/auroprice[1]*tradeamount - tradeamount * 0.005
                if eprofit > 0:
                    print("From BSC to Aurora possible")
                    print('BSC price: ', bscprice)
                    print('Aurora price: ',auroprice)
                    print("Expected profit: ",eprofit,'$')
            if polyprice[1]<auroprice[1]:
                eprofit = (bscprice[0] - polyprice[1])/polyprice[1]*tradeamount - tradeamount * 0.005
                if eprofit > 0:
                    print("From BSC to Polygon possible")
                    print('BSC price: ', bscprice)
                    print('Polygon price: ', polyprice)
                    print("Expected profit: ",eprofit,'$')
        elif auroprice[0]>polyprice[0]:
            if bscprice[1]<polyprice[1]:
                eprofit = (auroprice[0] - bscprice[1])/bscprice[1]*tradeamount - tradeamount * 0.005
                if eprofit > 0:
                    print("From Aurora to BSC possible")
                    print('Aurora price: ',auroprice)
                    print('BSC price: ', bscprice)
                    print("Expected profit: ",eprofit,'$')
            if polyprice[1]<bscprice[1]:
                eprofit = (auroprice[0] - polyprice[1])/polyprice[1] * tradeamount - tradeamount * 0.005
                if eprofit > 0:
                    print("From Aurora to Polygon possible")
                    print('Aurora price: ',auroprice)
                    print('Polygon price: ', polyprice)
                    print("Expected profit: ",eprofit,'$')
        else:
            if bscprice[1]<auroprice[1]:
                eprofit = (polyprice[0] - bscprice[1])/bscprice[1]* tradeamount - tradeamount * 0.005
                if eprofit > 0:
                    print("From Polygon to BSC possible")
                    print('Polygon price: ', polyprice)
                    print('BSC price: ', bscprice)
                    print("Expected profit: ",eprofit,'$')
            else:
                eprofit = (polyprice[0] - auroprice[1])/auroprice[1] * tradeamount - tradeamount * 0.005
                if eprofit > 0:
                    print('From Polygon to Aurora possible')
                    print('Polygon price: ', polyprice)
                    print('Aurora price: ',auroprice)
                    print("Expected profit: ",eprofit,'$')
        print("==================================================")
        time.sleep(5)
try:
    price()
except:
    time.sleep(10)
    price()