from multiprocessing import Pool, cpu_count
import time
from ebay_notifier.func import get_max_price, get_delay, get_info, get_listing_details, send_notification, check_changes, get_watchlist, get_already_searched, add_to_searched



def main():
	product_data = []

	watchlist = get_watchlist()
	for i in range(len(watchlist)):
		raw_product_data = [str(i) for i in get_info(watchlist[i]["url"])]
		with Pool(cpu_count()) as p:
			product_data.append(p.map(get_listing_details, raw_product_data))

	print("[+] Finished getting the initial listings from watchlist pages.")


	#main loop
	print("[+] Starting main check loop.")
	while True:
		for i in range(len(product_data)):
			new_raw_product_data = [str(i) for i in get_info(watchlist[i]["url"])]
			with Pool(cpu_count()) as p:
				new_product_data = p.map(get_listing_details, new_raw_product_data)

			new_listings = check_changes(new_product_data, product_data[i])

			if new_listings:
				max_price = watchlist[i]["max_price"]
				to_notify_about = []
				for l in new_listings:
					if float(l["price"][1:]) <= max_price:
						to_notify_about.append(l)
						print("[-] A new listing didnt meet the price requirement.")
				
				send_notification(to_notify_about)

				# the stored data is ONLY updated if there are mew listings. this prevents listings 
				product_data[i] = new_product_data

			else:
				print("[+] No new listings detected.")

			
		

		#gets the delay from config, then waits that amount before doing the whole cycle again
		delay = get_delay()
		print(f"[!] Waiting {delay} minutes.")
		time.sleep(60 * delay)



	#raw_product_data = [str(i) for i in get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&LH_BO=1&_ipg=120")]
	#
	#with Pool(cpu_count()) as p:
	#	product_data = p.map(get_listing_details, raw_product_data)
	#
	#print("[+] Finished getting the listings from the initial pages.")

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
				if float(l["price"][1:]) <= max_price and l["id"] not in get_already_searched():
					to_notify_about.append(l)
					print("[+] A listing is within the price critical region.")
					add_to_searched(l["id"])

			send_notification(to_notify_about)
		else:
			print("[+] No new listings detected.")

		# sets the new data to be the current data. the new_listings will hten be 
		product_data = new_product_data
		
		#gets the delay from config, then waits that amount before doing the whole cycle again
		delay = get_delay()
		print(f"[!] Waiting {delay} minutes.")
		time.sleep(60 * delay)
