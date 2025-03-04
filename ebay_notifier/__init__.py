import yaml
import os

def start():
	# creates config file
	if "config.yml" not in os.listdir():
		with open("config.yml", "w+") as cfg:
			cfg.write("""telegram_bot_token: \ntelegram_channel_id: \n""")
		print("[+] Config created.")

	from ebay_notifier.main import main
	main()
