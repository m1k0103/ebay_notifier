import yaml
import os
import sqlite3


def start():
	# creates config file
	if "config.yml" not in os.listdir():
		with open("config.yml", "w+") as cfg:
			cfg.write("""telegram_bot_token: \ntelegram_channel_id: \n""")
		print("[+] Config created.")

	# creates the db which will hold the last saved products
	if "last_saved.db" not in os.listdir():
		con = sqlite3.connect("last_saved.db")
		cur = con.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS products(
					id INTEGER PRIMARY KEY,
					title text,
					url text,
					price text,
					thumbnail text,
					shipping_fee,
					best_offers boolean
					)""")
		con.commit()
		con.close()

	#runs main
	from ebay_notifier.main import main
	main()
