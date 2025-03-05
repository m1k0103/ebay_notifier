import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool, cpu_count
import time
from urllib.parse import urlparse
import yaml
from ebay_notifier.func import get_random_proxy, get_max_price, get_delay, get_info, get_listing_details, send_notification, find_list_difference, check_changes


def main():
	raw_product_data = [str(i) for i in get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&LH_BO=1&_ipg=120")]
	
	with Pool(cpu_count()) as p:
		product_data = p.map(get_listing_details, raw_product_data)
	
	print("[+] Finished getting the listings from the initial page.")

	# main loop
	print("[+] Starting main check loop.")
	while True:
		new_raw_product_data = [str(i) for i in get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&LH_BO=1&_ipg=120")]
		with Pool(cpu_count()) as p:
			new_product_data = p.map(get_listing_details, new_raw_product_data)

		new_listings = check_changes(new_product_data, product_data)
		
		# if changes detected, this executes
		if new_listings:
			max_price = get_max_price()
			to_notify_about = []
			for l in new_listings:
				if float(l["price"][1:]) <= max_price:
					to_notify_about.append(l)
					print("[-] A new listing didnt meet the price requirement.")

			send_notification(to_notify_about)
		else:
			print("[+] No new listings detected.")

		# sets the new data to be the current data. the new_listings will hten be 
		product_data = new_product_data
		
		#gets the delay from config, then waits that amount before doing the whole cycle again
		delay = get_delay()
		print(f"[!] Waiting {delay} minutes.")
		time.sleep(60 * delay)
