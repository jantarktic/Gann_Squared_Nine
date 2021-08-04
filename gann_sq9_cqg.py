# -*- coding: utf-8 -*-
"""
Created on Tue Jul 6 22:07:00 2021

@author: jaydenclark
"""

from WebAPI.webapi_1_pb2 import *
from WebAPI import webapi_client
import threading
import datetime
import pandas as pd
from csv import writer
import os
import math

class setup:
    
    def __init__(self):
        #Enter user details
        self.user_name = ''
        self.password = ''
        self.client_app_id = ''
        self.private_label = ''
        self.client_version = ''
        #Using E-mini S&P as example ticker
        self.symbol_name = 'ep'
        self.subscribe = None
    
    def logon(self):
        client_msg = ClientMsg()
        client_msg.logon.user_name = self.user_name
        client_msg.logon.password = self.password
        client_msg.logon.client_app_id = self.client_app_id
        client_msg.logon.client_version = self.client_version
        client_msg.logon.private_label = self.private_label
        client.send_client_message(client_msg)
        server_msg = client.receive_server_message()
        if server_msg.logon_result.result_code == 0:
            return server_msg.logon_result.base_time
        else:
            raise Exception("Can't login: " + server_msg.logon_result.text_message)
    
    def logoff(self):
        client_msg = ClientMsg()
        client_msg.logoff.text_message = ("Logging Off")
        client.send_client_message(client_msg)
        server_msg = client.receive_server_message()

    def resolve_symbol(self):
        client_msg = ClientMsg()
        information_request = client_msg.information_request.add()
        information_request.id = 1
        if self.subscribe is not None:
            information_request.subscribe = self.subscribe
        information_request.symbol_resolution_request.symbol = self.symbol_name
        client.send_client_message(client_msg)

        server_msg = client.receive_server_message()
        return server_msg.information_report[0].symbol_resolution_report.contract_metadata

    def request_trade_subscription(self):
        client_msg = ClientMsg()
        request = client_msg.trade_subscription.add()
        request.id = 2
        request.subscribe = True
        request.subscription_scope.append(1) # 1 means order_status
        #request.subscription_scope.append(2) # 2 means positions_status
        #request.subscription_scope.append(3) # 3 means collateral_status
        request.publication_type = 4 
        client.send_client_message(client_msg)

        while True: 
            server_msg = client.receive_server_message()
            if server_msg.trade_snapshot_completion is not None:
                server_msg = client.receive_server_message()
                break

class gann(setup):

    def __init__(self):
        super().__init__()

        self.account_id = 1120072

        self.price_list = []
        self.volume_list = []

        self.volume = []
        self.bar_high = []
        self.bar_low = []
        self.bar_close = []

        self.gann_square_nine_levels = []
        self.message = []
        #set custom path
        self.log_data_path = '/gann_signals.csv'
            
        DATA_COLS = ['Minute', 'Price', 'Gann_Signals']
        if not os.path.exists(self.log_data_path):
            pd.DataFrame(columns=DATA_COLS).to_csv(self.log_data_path, header=DATA_COLS, index=False)

    def request_real_time(self):
        client_msg = ClientMsg()
        subscription = client_msg.market_data_subscription.add()
        subscription.contract_id = 1
        subscription.level = 1 #1 is trades/settlement quotes. 2 and 3 are BBA (3 is BBA with Volume).
        client.send_client_message(client_msg)
        executed = False
        while True: 
            server_msg = client.receive_server_message()
            try:
                #Adjust the next if statement to adjust the timeframe.
                #The statement is given a 3 second window in order to receive a tick quote. With illiquid instruments, use BBA data.
                if datetime.datetime.now().second >= 0 and datetime.datetime.now().second <= 3:
                    if executed == False:
                        self.onBar(self.price_list, self.volume_list) 
                        executed = True
                        if len(self.bar_close) > 1:
                            self.initializeGannSquareNine((server_msg.real_time_market_data[0].quote[0].scaled_price)/4)
                            timenday = datetime.datetime.now().strftime("%D %H:%M")
                            file = open(self.log_data_path, 'a+')
                            w = writer(file)
                            w.writerow([timenday, (server_msg.real_time_market_data[0].quote[0].scaled_price)/4, self.message])
                            file.close()
                            self.message.clear()                   
                    else:
                        self.price_list.append(server_msg.real_time_market_data[0].quote[0].scaled_price)
                        print(self.price_list[-1]/4)    

                else:
                    executed = False
                    self.price_list.append(server_msg.real_time_market_data[0].quote[0].scaled_price)
                    print(self.price_list[-1]/4) 
            #This exception avoids daily quotes that may interrupt the datastream and create an IndexError.
            except IndexError:
                print("Not really an Error. Just don't need that piece of data.")
    
    #This function creates the bars.
    def onBar(self, price_list, volume_list): 
        self.volume.append(sum(self.volume_list))
        self.bar_high.append(max(self.price_list))
        self.bar_low.append(min(self.price_list))
        self.bar_close.append(self.price_list[-1])

        print('1 minute bar:')
        print('Volume: ', self.volume)
        print('High: ', self.bar_high)
        print('Low: ', self.bar_low)
        print('Close: ', self.bar_close)

        if price_list is not None:
            self.price_list.clear()
            self.volume_list.clear()

    def initializeGannSquareNine(self, price):

        square = math.sqrt(price)
        
        a = ((square*180.0)-225.0)/360.0
        
        b = (a - math.trunc(a))*360
        
        base = (math.floor(square)-1.0) * (math.floor(square)-1.0)

        base_1 = math.sqrt(base)

        base_2 = base_1 + 1.0

        base_3 = base_1 + 2.0

        if self.gann_square_nine_levels is not None:
            self.gann_square_nine_levels.clear()
        else:
            pass

        angle = 0.125
        i = 0

        while i < 8:
            level = (base_1 + angle) * (base_1 + angle)
            self.gann_square_nine_levels.append(level)
            angle += 0.125
            i += 1

        angle = 0.125
        i = 0

        while i < 8:
            level = (base_2 + angle) * (base_2 + angle)
            self.gann_square_nine_levels.append(level)
            angle += 0.125
            i += 1

        angle = 0.125
        i = 0

        while i < 8:
            level = (base_3 + angle) * (base_3 + angle)
            self.gann_square_nine_levels.append(level)
            angle += 0.125
            i += 1

        self.gann_square_nine_levels.sort()

        for num in self.gann_square_nine_levels:
            self.message.append(num)

        print('Gann initialize. Square 9 levels are: ', self.message)
        print('The total amount of numbers are: ', len(self.message))
        
if __name__ == "__main__":
    client = webapi_client.WebApiClient()
    client.connect('wss://api.cqg.com:443')
    
    s = gann()

    baseTime = s.logon()
    contract_metadata = s.resolve_symbol()
    #Trade subscription runs asynchronously.
    status = threading.Thread(target=s.request_trade_subscription(), daemon=True)
    status.start()

    data = threading.Thread(target=s.request_real_time(), daemon=True)
    data.start()

    client.disconnect()