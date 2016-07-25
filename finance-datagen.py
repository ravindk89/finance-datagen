# Copyright (c) 2016 Ravind Kumar, MongoDB Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os
import sys
import random
import getopt
import datetime
import numpy
import json

from TradingCompany import Trader

from TradingClient import Client

#Globals

# Used for generating unique transaction IDs
transactions = set()


def generate_trading_companies():

    companies = []

    with open("trading_companies.txt") as f:
        trading_companies = f.read().splitlines()
        
    for f in trading_companies:
        f = json.loads(f)
        
        x = Trader(f["Trading Company"])
        
        for _ in range (0,3):
            x.add_trader(generate_trader())
        
        companies.append(x)
        
    return companies
    
def generate_trader():

    fname = ""
    lname = ""

    with open('fnames.txt') as f:
        fname = f.read().splitlines()
        f.close()

    with open('lnames.txt') as f:
        lname = f.read().splitlines()
        f.close()

    return random.choice(fname).lower().title() + \
           " " + \
           random.choice(lname).lower().title()
           
def generate_client_companies():

    companies = []

    with open("client_companies.txt") as f:
        client_companies = f.read().splitlines()
        
    for f in client_companies:
        f = json.loads(f)
        
        x = Client(f["Client Company"], f["clearing"])
        
        for _ in range (0,3):
            x.add_client(generate_client())
        
        companies.append(x)
        
    return companies
    
def generate_client():

    fname = ""
    lname = ""

    with open('fnames.txt') as f:
        fname = f.read().splitlines()
        f.close()

    with open('lnames.txt') as f:
        lname = f.read().splitlines()
        f.close()

    return random.choice(fname).lower().title() + \
           " " + \
           random.choice(lname).lower().title()

def generate_transaction_id():
    transaction_id = ""
    
    for _ in range(0,10):
        transaction_id += str(random.randint(1,9))

    global transactions
    
    while transaction_id in transactions:
        for _ in range(0,10):
            transaction_id += str(random.randint(1,9))
    
    transactions.add(transaction_id)
    
    return int(transaction_id)

def generate_trade(buy_trader, sell_trader, buy_client, sell_client):
    clearing = random.choice(["Mongo Exchange","MMX"])
    transaction = generate_transaction_id()
    product = random.choice(["MNG Natural Gas Futures","MNO Oil Futures"])
    unit_price = random.randint(1,10)
    trade_date = { "$date" : generate_date() }
    quantity = random.randint(25,15000)
    b_commission = 0.05 * quantity
    s_commission = 0.05 * quantity
    total_price = quantity * unit_price + b_commission + s_commission
    
    trade = {
        "buyer" : {
            "trader" : buy_trader.return_details(),
            "client" : buy_client.return_details(),
            "commission" : b_commission
        },
        "seller" : {
            "trader" : sell_trader.return_details(),
            "client" : sell_client.return_details(),
            "commission" : s_commission
        },
        "transaction_id" : transaction,
        "product" : product,
        "unit_price" : unit_price,
        "trade_date" : trade_date,
        "quantity" : quantity,
        "trade_total" : total_price
    }
    
    return json.dumps(trade)
    
def generate_date():
    year = random.choice(["2014", "2015", "2016"])
    month = random.choice(["01", "02", "03", "04", "05", "06", "07", "08",
                           "09", "10", "11", "12"])
    if month in ["01", "03", "05", "07", "08", "10", "12"]:
        day = random.randint(1, 31)
    elif month in ["02"]:
        day = random.randint(1, 28)
    else:
        day = random.randint(1, 30)

    return '{}-{}-{}T09:00:00.000-02:00'.format(year, month, str(day).zfill(2))

# Thanks to brian-khuu at stack overflow for this code
# http://stackoverflow.com/a/15860757

def update_progress(progress):
    """Displays or updates a console progress bar. Accepts a float between 0
       and 1.
       A value under 0 represents a 'halt'.
       A value 1 or bigger represents 100%."""
    bar_length = 10  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block +
                                              "-" * (bar_length - block),
                                              round(progress * 100, 1),
                                              status)
    sys.stdout.write(text)
    sys.stdout.flush()

def main(argv):
    
    limit = 100

    try:
        opts, _ = getopt.getopt(argv, "hl:d", ["limit=", "delete"])
    except getopt.GetoptError as exc:
        print(exc.msg)
        print("geo_datagen.py -l <limit> -d")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("finance_datagen.py -l <int> -d")
            print("-l | --limit \n" +
                  "\t The number of transactions to generate. \n")
            print("-d | delete \n" +
                  "\t Deletes the block_trades.json file" +
                  "if it already exists")
            print("\n finance_datagen.py creates a number of randomly generated \n" +
                  "financial transactions for use with the MongoDB mongoimport tool,  \n" +
                  "outputting the result to the block_trades.json file")
            sys.exit()
        elif opt in ("-l", "--limit"):
            print("Setting limit to " + arg)
            limit = int(arg)
        elif opt in ("-d", "--delete"):
            print("Removing block_trades.json")
            os.remove('block_trades.json')
    
    if limit > 10000000000:
        limit = 100000000000
        print ("Upper limit reached. Setting to 10,000,000,000")
    
    companies = generate_trading_companies()
    clients = generate_client_companies()

    with open('block_trades.json', 'a') as myfile:
        for x in range(0, limit):
            bt = random.choice(companies)
            st = random.choice(companies)
            bc = random.choice(clients)
            sc = random.choice(clients)
            myfile.write(generate_trade(bt,st,bc,sc) + "\n")
            update_progress(float(x) / float(limit))
        update_progress(1)
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))