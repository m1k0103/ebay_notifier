import os

def start():
	# creates config file
	if "config.yml" not in os.listdir():
		with open("config.yml", "w+") as cfg:
			cfg.write("""telegram_bot_token: \n
			telegram_channel_id: \n
			delay: # minutes\n
			watchlist: [\n
				{
				url: "",
			 	max_price:  # e.g. £10.00 would be 10.00
			 	}
			]""")
		print("[+] Config created.")

	#creates proxy file
	if "proxies.txt" not in os.listdir():
		with open("proxies.txt", "w+") as f:
			pass
		print("[+] Proxy file created.")

	#runs main
	from ebay_notifier.main import main
	main()
