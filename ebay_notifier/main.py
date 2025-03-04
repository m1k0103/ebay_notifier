import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool, cpu_count


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
	return all_li


# should recieve an index from all_li
def get_details_from_listing(listing):

	# CARRY ON FROM HERE. already have all the items from the search page, now just parse their raw data and stuff.
	pass


def main():
	raw_product_data = get_info("https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+ds+lite&_sacat=0&_from=R40&_trksid=p4384342.m570.l1313")
	with Pool(cpu_count()) as p:
		json_product_data = p.map(get_details_from_listing, raw_product_data)

	print(json_product_data)
