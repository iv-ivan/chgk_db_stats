import requests
from BeautifulSoup import BeautifulSoup
import codecs

page = requests.get("https://db.chgk.info/tour/") 
soup = BeautifulSoup(page.text)

tours = set()
for link in soup.findAll('a'):
    tour = link.get('href')
    if tour.startswith("/tour/"):
    	tours.add(tour)

txts = {}
for i, tour in enumerate(sorted(tours)):
	print i, "/", len(tours)
	try:
		page = requests.get("https://db.chgk.info/" + tour) 
		soup = BeautifulSoup(page.text)

		inner_tours = set()
		flag = False
		for link in soup.findAll('a'):
		    href = link.get('href')
		    if href and href.startswith("/tour/"):
		    	inner_tours.add(href)
		    if href and  ("/txt/" in href) and (".txt" in href):
				print href, "outer"
 				if href in txts:
					continue
				txts[href] = requests.get("https://db.chgk.info/" + href).text
				with codecs.open(href[5:], "w", encoding="utf-8") as f:
					f.write(txts[href])
				flag = True
		if flag:
			continue

		for inner_tour in  inner_tours:
			try:
				page = requests.get("https://db.chgk.info/" + inner_tour) 
				soup = BeautifulSoup(page.text)

				for link in soup.findAll('a'):
				    href = link.get('href')
				    if href and ("/txt/" in href) and (".txt" in href):
				    	print href, "inner"
				    	if href in txts:
				    		continue
				    	txts[href] = requests.get("https://db.chgk.info/" + href).text
				    	with codecs.open(href[5:], "w", encoding="utf-8") as f:
							f.write(txts[href])
			except Exception as e:
				print "Exeption", str(e), inner_tour
	except Exception as e:
		print "Exeption", str(e), tour
