import yaml
import os
import sqlite3


def start():
	# creates config file
	if "config.yml" not in os.listdir():
		with open("config.yml", "w+") as cfg:
			cfg.write("""telegram_bot_token: \ntelegram_channel_id: \n""")
		print("[+] Config created.")

	#runs main
	from ebay_notifier.main import main
	main()
