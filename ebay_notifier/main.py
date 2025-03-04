import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool, cpu_count
import sqlite3
import time

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
def get_details_from_listing(listing):
	listing = str(listing)
	listing_soup = BeautifulSoup(listing, "html.parser")


	listing_url = listing_soup.find("a", {"class":"s-item__link"})["href"]
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
		"best_offers":listing_best_offers
	}
	return product_dict


def save_data_to_db(data_dict):
	con = sqlite3.connect("last_saved.db")
	cur = con.cursor()
	cur.execute("INSERT INTO products(title,url,price,thumbnail,shipping_fee,best_offers) VALUES (:title,:url,:price,:thumbnail,:shipping_fee,:best_offers)", data_dict)
	con.commit()
	con.close()

def check_db_empty():
	con = sqlite3.connect("last_saved.db")
	cur = con.cursor()
	result = cur.execute("SELECT count(*) FROM products").fetchone()[0]
	
	if result != 0:
		return True
	else:
		return False


def send_notification():
	pass


def main():
	raw_product_data = get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&_sacat=0&LH_BO=1")
	
	with Pool(cpu_count()) as p:
		json_product_data = p.map(get_details_from_listing, raw_product_data) # PICKLER ERROR HERE.
	
	print("[+] Finished getting the listings from the initial page.")
	#product_data = [get_details_from_listing(raw_product_data[3])]

	if not check_db_empty():
		for pr in product_data:
			save_data_to_db(pr)
		print("[+] Initial products saved to DB.")
