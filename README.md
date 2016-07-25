# finance-datagen

This utility generates randomized JSON documents for use with MongoDB.

As the JSON is generated via a python dictionary, fields and values may
appear out of order. This has no effect on how MongoDB performs queries
on the document.

Each document contains the following fields and values:

    {
      "product": <string>,
      "unit_price": <int>,
      "trade_date": {
         "$date": "YYYY-MM-DDTHH:MM:SS.sss-02:00"
      },
    	"buyer": {
    		"commission": <int>,
    		"trader": {
    			"Trader": <string>,
    			"Company": <string>
    		},
    		"client": {
    			"Company": <string>,
    			"client": <string>
    		}
    	},
    	"trade_total": <int>,
    	"quantity": <int>,
    	"transaction_id": <int>,
    	"seller": {
    		"commission": <int>,
    		"trader": {
    			"Trader": <string>,
    			"Company": <string>
    		},
    		"client": {
    			"Company": <string>,
    			"client": <string>
    		}
    	}
    }

`finance-datagen` outputs the result into the `block-trades.json` file for
use with `mongoimport`.

# Usage

    python finance-datagen.py -h -l <int> -d -u

* `-h` : Provides help
* `-l` | `--limit` : Creates `n` number of documents. Supports up to
    10,000,000,000 documents.
* `-d` | `--delete` : Deletes `block-trades.json`

# Notes

## Date

The `trade_date` field contains the `$date` field. The 
`mongoimport` utility reads this in as an `ISODate()` object. 

## Pricing

The `trade_total` field consists of `quantity` * `unit_price` + `buyer.commission` + `seller.commission`. 

Commission is calculated at 0.05 * `quantity` for a per-lot commission.

## Buyer and Seller

All Trader and Client information is completely randomized.

In future versions, additional generating actions will allow for 
random generation of Trader and Client information, allowing for more 
varied results. 

At this time, the client / trader can be the same for both buyer and seller.

## Transaction ID

The `transaction_id` is a randomly generated 10 digit ID and supports
up to 10,000,000,000 documents.


# Disclaimer

This product is meant for educational or development purposes only. Any
resemblance to real or fictional persons, living or dead is purely
coincidental. No other warranty expressed or implied. May be too intense for
some viewers. If condition persists, consult your physician. No
user-serviceable parts inside. Freshest if eaten before date on carton.
Subject to change without notice. Contains a substantial amount of non-tobacco
ingredients. Slippery when wet. Not responsible for direct, indirect,
incidental or consequential damages resulting from any defect, error or
failure to perform. Not the Beatles. Penalty for private use. See label for
sequence. Use only in a well-ventilated area. Keep away from fire or flames.
Replace with same type. Do not fold, spindle or mutilate. No transfers issued
until the bus comes to a complete stop. Although robust enough for general
use, adventures into the esoteric periphery may reveal unexpected quirks.
Vitamins A, D, E, and K may have been added. Not designed or intended for use
in on-line control of aircraft, air traffic, aircraft navigation or aircraft
communications; or in the design, construction, operation or maintenance of
any nuclear facility. May contain traces of various nuts and seeds.

This supersedes all previous notices.
