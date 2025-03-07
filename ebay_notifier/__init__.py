import os

def start():
	# creates config file
	if "config.yml" not in os.listdir():
		with open("config.yml", "w+") as cfg:
			cfg.write("""telegram_bot_token: \ntelegram_channel_id: \ndelay: # minutes\nwatchlist: [\n{\nurl: "https://example.com",\nmax_price:  # e.g. £10.00 would be 10.00\n}\n]""")
		print("[+] Config created.")

	#creates resources directory
	if "resources" not in os.listdir("ebay_notifier"):
		os.chdir("ebay_notifier")
		os.mkdir("resources")
		os.chdir("..")

	#creates proxy file
	if "proxies.txt" not in os.listdir("ebay_notifier/resources"):
		with open("ebay_notifier/resources/proxies.txt", "w+") as f:
			print("[+] Proxy file created.")

	#creates searched file
	if "searched.txt" not in os.listdir("ebay_notifier/resources"):
		with open("ebay_notifier/resources/resources.txt", "w+") as f:
			print("[+] Searched file created.")

	#runs main
	from ebay_notifier.main import main
	main()
