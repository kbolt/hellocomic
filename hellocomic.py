#! python3
# hellocomic.py - Downloads every page for a specific comic from hellocomic.com

import os
import requests
import bs4
import urllib.parse

url = 'http://www.hellocomic.com/painkiller-jane-the-22-brides/c2/p1'
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

# Generate folder name
title = url.rsplit('/')[3]
chapter =  url.rsplit('/')[-2]
folderName = title + " " + "-" + " " + chapter

headers = { 'User-Agent' : user_agent }
os.makedirs(folderName, exist_ok=True)   # store comics in folder
while not url.endswith('p'+str([0-9])):
	# Download the page
	print('Downloading page %s' % url)
	res = requests.get(url)
	res.raise_for_status()
	print(res)
	soup = bs4.BeautifulSoup(res.text, "html.parser")

	# Find the URL of the comic image.
	comicElem = soup.select('.coverIssue img')
	if comicElem == []:
		print('Could not find comic image.')
	else:
		try:
			comicUrl = comicElem[0].get('src')
			# Download the image.
			print('Downloading image %s' % (comicUrl))
			res = requests.get(comicUrl)
			res.raise_for_status()
		except requests.exceptions.MissingSchema:
			# skip this comic
			nextLink = soup.select('.nextBtn')[0]
			url = nextLink.get('href')
			continue
		# Save the image to folder.
		imageFile = open(os.path.join(folderName, os.path.basename(comicUrl)), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

	# Get the Next button's url.
	nextLink = soup.select('.nextBtn')[0]
	url = nextLink.get('href')

print('Done.')
