# ebay_notifier
A messy script which notifies you of new Ebay listings, and sends the listing details to a Telegram channel via a bot.


## Setup
1) Create a virtual environment (optional but recommended).
2) Install requirements in `requirements.txt`.
3) Run `start.py`, it should fail on the first run of the program and should create a `config.yml` file.
4) Use an Ebay search link* to enter into the config, along with a max price of the item.
5) Enter your Telegram bot token, channel ID, and the delay between each check (I recommend 5 to 20 minutes depending on how popular your item is).
5) Run the `autorun.sh` file.
6) Success!!

> [!IMPORTANT]
> Make sure to use proxies if you are planing on checking for new listings more frequently!

## Adding multiple links to search.

To add multiple links for the program to look at, format them in the following way:
`
watchlist: [ { url: "foobar1", max_price: 2 }, { url: "foobar2", max_price: 2 } ]
`
It is essencially just an array containing multiple dictionaries, where the dicitonaries contain the url you want to search and the max price to notify you of. 
