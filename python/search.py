#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python /var/www/charity/python/search.py
"""
* @python name:		py/search.py
* @description:		This file has common def.
* @related issues:	Charity-001
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/27/2015
* @called by:
"""
# For Python3
# sudo pip install requests xlsxwriter beautifulsoup4 python-dateutil pdfkit
# sudo apt-get install wkhtmltopdf
# https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
# sudo pip uninstall wkhtmltopdf
# sudo apt-get install python3 python3-pip
# sudo mv /usr/bin/python /usr/bin/python_2.7; sudo ln -fs /usr/bin/python3.4 /usr/bin/python

# https://xlsxwriter.readthedocs.org/
# https://developers.google.com/custom-search/docs/xml_results#WebSearch_Request_Format
import requests
from bs4 import BeautifulSoup, Comment
import urllib.parse
# import urllib		# Python 2
import xlsxwriter
# import xlwt3
# import xlwt		# Python 2
import pdfkit
# import wkhtmltopdf

import sys
import os
import re
import time
from datetime import datetime
from datetime import timedelta
import json
import shutil
from dateutil.relativedelta import *


"""
* @def name:		getQueryUrl(keywords)
* @description:		This function returns an URL for Google search.
* @related issues:	Charity-001
* @param:			string keywords
* @return:			string url
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/26/2015
* @called by:		def getSearchResult(keywords, limit)
*					 in charity/python/search.py
"""
def getQueryUrl(keywords):
	keywords = keywords.split(' ')
	for key, word in enumerate(keywords):
		keywords[key] = urllib.parse.quote(word)

	print(keywords)
	keywords = '+'.join(keywords)
	filetypes = ['pdf', 'ppt', 'pptx', 'doc', 'docx']
	filetypes = '+OR+filetype:'.join(filetypes)
	# query = keywords + '+filetype:' + filetypes
	query = keywords
	print(query)
	# url = 'https://www.google.com.tw/search?'
	url = 'https://www.google.com.tw/search?ie=UTF-8&client=google-csbe'
	# url += 'start=0&num=10&ie=UTF-8&client=google-csbe'
	# url += 'start=0&num=20&client=google-csbe'
	# url = 'http://www.google.com/search?start=0&num=20&client=google-csbe&cx=00255077836266642015:u-scht7a-8i'
	url += '&q=' + query
	# url += '&tbs=qdr:y'		# within last year
	return url

"""
* @def name:		getSearchResult(keywords, limit)
* @description:		This function returns a list of search results.
* @related issues:	Charity-001
* @param:			string keywords
* @param:			integer limit
* @return:			list rows
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/26/2015
* @called by:		main
*					 in charity/python/search.py
"""
def getSearchResult(keywords, limit):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
		"Accept-Encoding": "gzip, deflate",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive"
	}

	# headers = {
	# 	"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0",
	# 	"Accept-Encoding": "gzip, deflate",
	# 	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	# 	"Accept-Language": "en-US,en;q=0.5",
	# 	"Connection": "keep-alive"
	# }
	# payload = {'query': ip}
	# payload = {
	# 	'datestart': '2015/3/18',
	# 	'dateend': '2015/4/17'
	# }
	urlQuery = getQueryUrl(keywords)
	start = 0
	num = 0
	count = limit + 5
	rows = []
	while count > 0:
		if count > 20:
			num = 20
		else: num = count
		# url += '&start=0&num=20'
		urlRequest = urlQuery + '&start=' + str(start) + '&num=' + str(num)
		print(urlRequest)

		r = requests.get(urlRequest)
		# soup = BeautifulSoup(r.text)	# Python2
		soup = BeautifulSoup(r.text, "lxml")
		results = soup.findAll('li', {'class': 'g'})
		# print(results)
		# print(len(results))
		for key, element in enumerate(results):
			# print(key)
			# print(element)
			if element.find('cite') is not None:
				title = element.find('a').getText().strip()
				url = element.find('cite').getText().strip()
				print(title)
				print(url)
				url2 = element.find('a')['href'].strip()
				if '...' in url:
					url = 'https://www.google.com.tw' + url2
					try:
						r = requests.get(url, headers=headers, timeout=10)
						url = r.history[-1].headers['Location'].strip('/')
						print(url)

					except requests.exceptions.Timeout as e:
						# Maybe set up for a retry, or continue in a retry loop
						print('Exception: Timeout')
						print(e)
						url = 'Not Available'
					except requests.exceptions.ConnectionError as e:
						# A Connection error occurred.
						print('Exception: ConnectionError')
						print(e)
						url = 'Not Available'
					except requests.exceptions.HTTPError as e:
						# An HTTP error occurred.
						print('Exception: HTTPError')
						print(e)
						url = 'Not Available'
					except requests.exceptions.TooManyRedirects as e:
						# Too many redirects.
						# Tell the user their URL was bad and try a different one
						print('Exception: TooManyRedirects')
						print(e)
						url = 'Not Available'
					except requests.exceptions.URLRequired as e:
						# A valid URL is required to make a request.
						print('Exception: Valid URL Required')
						print(e)
						url = 'Not Available'
					except requests.exceptions.RequestException as e:
						# There was an ambiguous exception that occurred while handling your request.
						# catastrophic error. bail.
						print('Exception: Ambiguous requests exception')
						print(e)
						url = 'Not Available'
					except IOError as e:
						print("I/O error({0}): {1}".format(e.errno, e.strerror))
						print('Cannot find URL')
						print(type(e))
						print(e)
						url = 'Not Available'
					except:
						print("Unexpected error:", sys.exc_info()[0])
						url = 'Not Available'

				text = element.find('span', {'class': 'st'}).getText().replace('\n', '').strip()
				# text = text.replace('. ', '').strip()
				print(text)
				print(url)
				if url != 'Not Available' and '.' in url:
					if 'http' not in url: url = 'http://' + url
					row = [title, text, url.lower()]
					rows.append(row)
		start += num
		count -= num
	return rows[:limit]


"""
* @def name:		writeXls(xls, keywords, rows)
* @description:		This function exports data from table to xls file.
* @related issues:	Charity-001
* @param:			string xls
* @param:			string keywords
* @param:			list rows
* @return:			void
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/26/2015
* @called by:		main
*					 in charity/python/search.py
"""
def writeXls(xls, keywords, rows):
	print(rows)
	cntRows = len(rows)
	date = getNow('%y%m%d_%H%M')
	# xls += '_' + date + '.xls'
	xls += '_' + str(cntRows) + '_' + date + '.xls'
	fields = ['Title', 'Description', 'URL']
	workbook = xlsxwriter.Workbook(xls)
	# worksheet = workbook.add_worksheet(keywords)
	sheet = workbook.add_worksheet(keywords)
	# Widen the first column to make the text clearer.
	# sheet.set_column('A:A', 40)
	sheet.set_column('A:A', 50)
	# sheet.set_column('B:B', 60)
	# sheet.set_column('B:B', 100)
	# sheet.set_column('B:B', 150)
	sheet.set_column('B:B', 130)

	col = 0
	for field in fields:
		sheet.write(0, col, field)
		col += 1

	key = 1
	for row in rows:
		col = 0
		for cell in row:
			#cell = cutString(cell, 3000)
			sheet.write(key, col, cell)
			col += 1
		key += 1
	print(xls)
	# workbook.save(xls)
	workbook.close()

"""
* @def name:		getNow(format=None)
* @description:		This function returns a string of time of now.
* @related issues:	Charity-001
* @param:			string format=None
* @return:			string now
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/24/2015
* @called by:		def writeXls(xls, keywords, rows)
*					 in charity/python/search.py
"""
def getNow(format=None):
	#if format is None: format = '%Y/%m/%d %a %H:%M:%S'
	if format is None: format = '%Y-%m-%d %H:%M:%S'
	now = datetime.now().strftime(format)
	return now

"""
* @def name:		getLocalFileName(title, url)
* @description:		This function downloads files to given folder.
* @related issues:	Charity-001
* @param:			string title
* @param:			string url
* @return:			string localFileName
* @author:			Don Hsieh
* @since:			07/27/2015
* @last modified:	07/27/2015
* @called by:		def getFiles(folder, results)
*					 in charity/python/search.py
"""
def getLocalFileName(title, url, key, folder):
	name = title.split(' ')[0]
	# print(name)
	name = name.split('(')[0].split(u'（')[0].split('/')[0]
	name = name.split('!')[0].split('?')[0].split('.')[0].split('*')[0]
	print(name)
	print(url)
	localFileName = urllib.parse.unquote(url.split('/')[-1]).split('?')[0].replace(' ', '-')
	# if len(name) != len(localFileName.split('.')[0]):
	if name != localFileName.split('.')[0]:
		if len(name) > 3:
			localFileName = name + '_' + localFileName
	localFileName = str(key+1) + '_' + localFileName
	localFileName = localFileName.replace('__', '_')
	localFileName = os.path.join(folder, localFileName)
	print(localFileName)
	return localFileName

"""
* @def name:		getFiles(folder, results)
* @description:		This function downloads files to given folder.
* @related issues:	Charity-001
* @param:			string folder
* @param:			list results
* @return:			void
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/26/2015
* @called by:		main
*					 in charity/python/search.py
"""
def getFiles(folder, results):
	print(folder)
	print(results)
	if not os.path.exists(folder):
		os.makedirs(folder)
	# row = [title, text, url]
	# for result in results:
	
	for key, result in enumerate(results):
		title = result[0]
		url = result[2]
		localFileName = getLocalFileName(title, url, key, folder)

		try:
			# NOTE the stream=True parameter
			r = requests.get(url, stream=True)
			with open(localFileName, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
						f.flush()
		except requests.exceptions.Timeout as e:
			# Maybe set up for a retry, or continue in a retry loop
			print('Exception: Timeout')
			print(e)
		except requests.exceptions.ConnectionError as e:
			# A Connection error occurred.
			print('Exception: ConnectionError')
			print(e)
		except requests.exceptions.HTTPError as e:
			# An HTTP error occurred.
			print('Exception: HTTPError')
			print(e)
		except requests.exceptions.TooManyRedirects as e:
			# Too many redirects.
			# Tell the user their URL was bad and try a different one
			print('Exception: TooManyRedirects')
			print(e)
		except requests.exceptions.URLRequired as e:
			# A valid URL is required to make a request.
			print('Exception: Valid URL Required')
			print(e)
		except requests.exceptions.RequestException as e:
			# There was an ambiguous exception that occurred while handling your request.
			# catastrophic error. bail.
			print('Exception: Ambiguous requests exception')
			print(e)
		except IOError as e:
			print("I/O error({0}): {1}".format(e.errno, e.strerror))
			print('Cannot find URL')
			print(type(e))
			print(e)
		except:
			print("Unexpected error:", sys.exc_info()[0])


"""
* @def name:		exportHtmlToPdf(results, folder)
* @description:		This function downloads files to given folder.
* @related issues:	Charity-001
* @param:			string folder
* @param:			list results
* @return:			void
* @author:			Don Hsieh
* @since:			07/27/2015
* @last modified:	07/27/2015
* @called by:		main
*					 in charity/python/search.py
"""
def exportHtmlToPdf(results, folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
	options = {
		'page-size': 'Letter',
		'margin-top': '0.75in',
		'margin-right': '0.75in',
		'margin-bottom': '0.75in',
		'margin-left': '0.75in',
		'encoding': 'UTF-8',
		# 'quiet': ''
	}

	# options = {
	# 	'page-size': 'Letter',
	# 	'margin-top': '0.75in',
	# 	'margin-right': '0.75in',
	# 	'margin-bottom': '0.75in',
	# 	'margin-left': '0.75in',
	# 	'encoding': "UTF-8",
	# 	'quiet': ''		# turn off wkhtmltopdf output
	# }
	for key, result in enumerate(results):
		title = result[0]
		url = result[2]
		# localFileName = getLocalFileName(title, url, key, '/var/www/charity/python') + '.pdf'
		# localFileName = os.path.join('/var/www/charity/python', str(key+1) + '.pdf')
		# localFileName = os.path.join(str(key+1) + '.pdf')
		localFileName = str(key+1) + '.pdf'
		print(title)
		print(url)
		print(localFileName)
		# pdfkit.from_url(url, localFileName)
		# pdfkit.from_url(url, '/var/www/charity/python/files_偏鄉教育_10_150727_2147/out.pdf')
		# pdfkit.from_url(url, '/var/www/charity/python/out.pdf')
		# raise
		pdfkit.from_url(url, localFileName, options=options)
		# pdfkit.from_url(['google.com', 'yandex.ru', 'engadget.com'], 'out.pdf')

# url = 'http://www.thenewslens.com/post/108773/'
# # localFileName = './out.pdf'
# # localFileName = 'out.pdf'
# localFileName = '/var/www/charity/python/out.pdf'
# localFileName = '/var/www/charity/python/out2.pdf'
# localFileName = '/var/www/charity/python/out3.pdf'
# options = {
# 	'page-size': 'Letter',
# 	'margin-top': '0.75in',
# 	'margin-right': '0.75in',
# 	'margin-bottom': '0.75in',
# 	'margin-left': '0.75in',
# 	'encoding': "UTF-8",
# 	# 'no-outline': None
# 	# 'quiet': ''		# turn off wkhtmltopdf output
# }
# pdfkit.from_url(url, localFileName, options=options)
# # pdfkit.from_url(url, localFileName)
# raise

keywords = '偏鄉教育'
# keywords = 'Material Design Lite'
# keywords = 'Material Design Lite Google Web UI'
# keywords = 'React.js web js fb dom'
# keywords = 'ReactJS NodeJS'
# keywords = 'Grafana'
# keywords = u'偏鄉教育'
# keywords = keywords.decode('utf-8').encode('utf-8')
# keywords = unicode(keywords)
# .encode("utf-8")
# results = []
# print(os.getcwd())

path = os.path.dirname(os.path.realpath(__file__))
xls = os.path.join(path, keywords)

# results = getSearchResult(keywords)
# results = getSearchResult(keywords, 10)
# results = getSearchResult(keywords, 30)
# results = getSearchResult(keywords, 50)
results = getSearchResult(keywords, 100)
print(results)
print(len(results))
# raise
writeXls(xls, keywords, results)
folder = 'files_' + keywords.replace(' ', '_') + '_' + str(len(results)) + '_' + getNow('%y%m%d_%H%M')
folder = os.path.join(path, folder)
# raise
# exportHtmlToPdf(results, folder)
# raise

# results = [['偏鄉數位關懷推動計畫(101 年- 104 年) - 行政院',
# 		'弱勢學童資訊教育與學習扶助。招募資訊志工團隊，以學生專業資訊能力，. 協助偏鄉民眾數位應用及協助地方特色數位化發展與行銷。結合本部和民. 間資源共同推動 ...',
# 		'http://www.ey.gov.tw/Upload/RelFile/26/704681/14e83fdc-bb52-4e4e-9428-ac222ca6c817.pdf'
# 	]]
getFiles(folder, results)

print("Done")