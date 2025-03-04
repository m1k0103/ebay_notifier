import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool, cpu_count
import time
from urllib.parse import urlparse
import yaml

def get_random_proxy():
	pass


def get_info(url):
	#sends request and turns into soup
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")

	# regex to be used to identify the products
	data_viewport_regex = re.compile('.*{"trackableId":".*')
	id_regex = re.compile('.*item.*')
	
	#all products extracted from soup using the regex
	all_li = soup.find_all("li", {"data-viewport": data_viewport_regex, "id": id_regex})

	#print(str(all_li), "\n\n\n")
	#print(str(all_li[0]))
	print(len(all_li))
	return all_li


# should recieve an index from all_li
def get_listing_details(listing):
	listing = str(listing)
	listing_soup = BeautifulSoup(listing, "html.parser")

	listing_url = urlparse(listing_soup.find("a", {"class":"s-item__link"})["href"])._replace(query="").geturl()

	listing_id = urlparse(listing_url)[2].split("/")[2]
	listing_price = listing_soup.find("span", {"class":"s-item__price"}).text
	listing_title = listing_soup.find("div", {"class":"s-item__title"}).text

	thumbnail_regex = re.compile('.*i.ebayimg.com.*')
	listing_thumbnail = listing_soup.find("img", {"src":thumbnail_regex})["src"]

	try:
		listing_shipping_fee = listing_soup.find("span", {"class":"s-item__dynamic s-item__paidDeliveryInfo"}).text
	except:
		listing_shipping_fee = False # this means free shipping
	try:
		BO_regex = re.compile('.*s-item__formatBestOfferEnabled.*')
		listing_best_offers = listing_soup.find("span", {"class":BO_regex})
		listing_best_offers = True
	except:
		listing_best_offers = False
	
	#maybe add seller too
	product_dict = {
		"title":listing_title,
		"url":listing_url,
		"price":listing_price,
		"thumbnail":listing_thumbnail,
		"shipping_fee":listing_shipping_fee,
		"best_offers":listing_best_offers,
		"id":listing_id
	}
	return product_dict


def send_notification(listings):
	with open("config.yml") as config:
		try:
			contents = yaml.safe_load(config)
			bot_token = contents["telegram_bot_token"]
			channel_id = contents["telegram_channel_id"]
		except Exception as e:
			print(f"[-] Config error: {e}")
		# title
		# Current price
		# If allows offers
		# Link
		# Thumbnail
		for item in listings:
			message = f"""{item['title']}\n\nPrice: {item['price']}\nOffers enabled: {item['best_offers']}\n{item['thumbnail']}\n\n{item['url']}"""

			url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={message}"
			resp = requests.get(url)

			if resp.ok:
				print("[+] New listing. Sent notification.")
			else:
				print("[-] Failed to send notification.")



#essencially l1 - l2
def find_list_difference(l1,l2):
	result=[]
	for i in l1:
		if i not in l2:
			result.append(i)
	return result



def check_changes(new_data, old_data):
	sorted_old = sorted(old_data, key=lambda d: d['id'])
	sorted_new = sorted(new_data, key=lambda d: d['id'])
	if sorted_old == sorted_new:
		return False
	else: # find difference between them as they are not the same
		old_ids = {item['id'] for item in sorted_old}
		#new_ids = {item['id'] for item in sorted_new}

		added_items = [item for item in sorted_new if item['id'] not in old_ids]
		print("\nAdded Items:")

		new_listings = []
		for item in added_items:
			new_listings.append(item)

		return new_listings

def main():
	raw_product_data = [str(i) for i in get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&_sacat=0&LH_BO=1")]
	
	with Pool(cpu_count()) as p:
		product_data = p.map(get_listing_details, raw_product_data)
	
	print("[+] Finished getting the listings from the initial page.")

	# main loop
	print("[+] Starting main check loop.")
	while True:
		new_raw_product_data = [str(i) for i in get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&_sacat=0&LH_BO=1")]
		with Pool(cpu_count()) as p:
			new_product_data = p.map(get_listing_details, new_raw_product_data)

		new_listings = check_changes(new_product_data, product_data)
		if new_listings:
			# if changes detected, this executes
			send_notification(new_listings)

		product_data = new_listings
		time.sleep(60) # after the 60 seconds,it spams messages. i dont know why.