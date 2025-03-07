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
				max_price = get_max_price(i)
				to_notify_about = []
				for l in new_listings:
					if float(l["price"][1:]) <= max_price and l["id"] not in get_already_searched():
						to_notify_about.append(l)
						print("[+] A listing is within the price critical region.")
						add_to_searched(l["id"])

				send_notification(to_notify_about)
			else:
				print("[+] No new listings detected.")

			
		

		#gets the delay from config, then waits that amount before doing the whole cycle again
		delay = get_delay()
		print(f"[!] Waiting {delay} minutes.")
		time.sleep(60 * delay)



