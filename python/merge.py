#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python ~/code/charity/python/merge.py
"""
* @python name:		py/merge.py
* @description:		This file is a web crawler for mergers and acquisitions data.
* @related issues:	Charity-002
* @author:			Don Hsieh
* @since:			02/20/2016
* @last modified:	02/21/2016
* @called by:
"""
# For Python3
# sudo pip install requests xlsxwriter beautifulsoup4 python-dateutil pdfkit
#
# for Mac
# brew install python3
# sudo pip3 install requests xlsxwriter beautifulsoup4 python-dateutil pdfkit
# pip install --upgrade lxml
## sudo port install py27-lxml
#
# sudo apt-get install python3 python3-pip
# sudo mv /usr/bin/python /usr/bin/python_2.7; sudo ln -fs /usr/bin/python3.4 /usr/bin/python

import csv
import codecs
import requests
from bs4 import BeautifulSoup, Comment
# import urllib.parse		# Python 3
import urllib		# Python 2
from urlparse import urlparse		# Python 2

import sys
import os
# import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import *

"""
* @def name:		getQueryUrl(keywords)
* @description:		This function returns an URL for Google search.
* @related issues:	Charity-002
* @param:			string keywords
* @return:			string url
* @author:			Don Hsieh
* @since:			02/24/2016
* @last modified:	02/26/2016
* @called by:		def getSearchResult(keywords, limit)
*					 in charity/python/search.py
"""
def getQueryUrl(page):
	url = 'http://www.chinaventure.com.cn/cvsourcemodel/merge/list/0/'
	url += str(page) + '.shtml'
	return url

"""
* @def name:		parseElement(element)
* @description:		This function returns cite URL of a Google
*					 search result.
* @related issues:	Charity-002
* @param:			integer key
* @param:			bs4.element.Tag element
* @return:			tuple title, url
* @author:			Don Hsieh
* @since:			10/10/2016
* @last modified:	10/10/2016
* @called by:		getSearchResult(keywords, limit)
*					 in charity/python/search.py
"""
def parseDetails(element):
	if  len(element.findAll('td')) > 0:
		content = element.findAll('td')[-1].getText().replace('\n', '').strip()
		return content
	else:
		print "element hs no td :", element
		print '\n\n'
		raise

"""
* @def name:		getDatailPageContent(url)
* @description:		This function returns statusCode, contentLength,
*					 contentType, and contentDisposition of an URL.
* @related issues:	Charity-002
* @param:			string title
* @param:			string description
* @param:			string url
* @return:			list row
* @author:			Don Hsieh
* @since:			10/09/2016
* @last modified:	10/10/2016
* @called by:		def getCiteUrl(key, element)
*					 in charity/python/search.py
"""
def getDatailPageContent(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
		"Accept-Encoding": "gzip, deflate",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive"
	}
	titlesFull = ['target', 'buyer', 'amount', 'industry', 'date', 'url', 'type', 'trade_way', 'cross_nation', 
	'associate_trade', 'attitude', 'status', 'declare_date', 'end_date', 'amount', 'valuation', 'pay_way', 
	'industry_detail', 'target', 'buyer', 'bank', 'lawyer', 'accountant', 'estimator', 'description']
	# titles = ['target', 'buyer', 'amount', 'industry', 'date', 'url']
	titles = ['type', 'trade_way', 'cross_nation', 'associate_trade', 'attitude', 'status', 'declare_date', 
	'end_date', 'amount', 'valuation', 'pay_way', 'industry_detail', 'target', 'buyer', 'bank', 'lawyer', 
	'accountant', 'estimator', 'description']
	try:
		rows = []
		url = 'http://www.chinaventure.com.cn' + url
		r = requests.get(url, headers=headers, timeout=10, verify=False)

		statusCode = r.status_code
		contentLength = None
		if 'content-length' in r.headers:
			contentLength = r.headers['content-length']
		contentType = None
		if 'content-type' in r.headers:
			contentType = r.headers['content-type']
		contentDisposition = None
		if 'content-disposition' in r.headers:
			contentDisposition = r.headers['content-disposition']

		s = str(statusCode)
		if contentType is not None:
			s += '\t' + contentType
		if contentDisposition is not None:
			s += '\t' + contentDisposition
		if contentLength is not None:
			s += '\t' + contentLength
		print(s)

		soup = BeautifulSoup(r.text, "lxml")
		results = soup.find('tbody').findAll('tr')
		for i, element in enumerate(results):
			s = parseDetails(element)
			# print titles[i] + " = " + s
			if s is not None:
				rows.append(s)
		div = soup.find('div', {'class': 'left680'}).contents[18:]
		descriptions = []
		for line in div:
			# <class 'bs4.element.Tag'>
			if type(line) != type(soup.find('div', {'class': 'left680'}).contents[17]):
				line = line.replace(u'\n', '').replace(u'\r', '').replace(u'\t', '').strip()
				if len(line) > 2:
					descriptions.append(line)
		# description = '\n'.join(descriptions).replace(u'\n\n', '\n').strip()
		description = '<br>'.join(descriptions).strip()
		rows.append(description)
		return rows
	except requests.exceptions.Timeout as e:
		# Maybe set up for a retry, or continue in a retry loop
		print('Exception - Timeout: ', e)
		print 'url =', url
		# raise
		return None
	except requests.exceptions.ConnectionError as e:
		print('Exception - ConnectionError: ', e)
		print 'url =', url
		# raise
		return None
	except requests.exceptions.HTTPError as e:
		print('Exception - HTTPError: ', e)
		raise
	except requests.exceptions.TooManyRedirects as e:
		print('Exception - TooManyRedirects: ', e)
		# Exception - TooManyRedirects:  Exceeded 30 redirects.
		return None
		# raise
	except requests.exceptions.URLRequired as e:
		print('Exception - Valid URL Required: ', e)
		raise
	except requests.exceptions.RequestException as e:
		print('Exception - Ambiguous requests exception: ', e)
		raise
	except IOError as e:
		print("I/O error: ", e)
		return None
	except:
		print("Unexpected error:", sys.exc_info()[0])


"""
* @def name:		parseElement(element)
* @description:		This function returns cite URL of a Google
*					 search result.
* @related issues:	Charity-002
* @param:			integer key
* @param:			bs4.element.Tag element
* @return:			tuple title, url
* @author:			Don Hsieh
* @since:			10/10/2016
* @last modified:	10/10/2016
* @called by:		getSearchResult(keywords, limit)
*					 in charity/python/search.py
"""
def parseElement(element):
	# titles = ['target', 'buyer', 'amount', 'industry', 'date', 'url', 'type', 'trade_way', 'cross_nation', 'associate_trade', 'attitude', 'status', 'declare_date', 'end_date', 'amount', 'valuation', 'pay_way', 'industry_detail', 'target', 'buyer', 'bank', 'lawyer', 'accountant', 'estimator', 'description']
	titlesFull = ['target', 'buyer', 'amount', 'industry', 'date', 'url', 'type', 'trade_way', 'cross_nation', 
	'associate_trade', 'attitude', 'status', 'declare_date', 'end_date', 'amount', 'valuation', 'pay_way', 
	'industry_detail', 'target', 'buyer', 'bank', 'lawyer', 'accountant', 'estimator', 'description']
	titles = ['target', 'buyer', 'amount', 'industry', 'date', 'url']
	row = []
	if len(element.findAll('td')) > 0:
		contents = element.findAll('td')
		for i, content in enumerate(contents):
			if len(content.contents) > 1:
				content = content.find('a')['href'].replace('\n', '').strip()
			else:
				content = content.getText().replace('\n', '').strip()
			# print titles[i] + " = " + content
			row.append(content)
		url = row[-1]
		details = getDatailPageContent(url)
		if details is not None and len(details) > 0:
			row.extend(details)
		else:
			print 'details is None'
			print 'row =', row
	return row

"""
* @def name:		getPageContent(pageNumber)
* @description:		This function returns a list of search results.
* @related issues:	Charity-002
* @param:			string keywords
* @param:			integer limit
* @return:			list rows
* @author:			Don Hsieh
* @since:			02/24/2016
* @last modified:	02/26/2016
* @called by:		main
*					 in charity/python/search.py
"""
def getPageContent(pageNumber):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
		"Accept-Encoding": "gzip, deflate",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive"
	}
	urlQuery = getQueryUrl(pageNumber)
	print(urlQuery)
	r = requests.get(urlQuery, headers=headers, timeout=20)
	# soup = BeautifulSoup(r.text)	# Python2
	soup = BeautifulSoup(r.text, "lxml")
	results = soup.find('tbody').findAll('tr')
	rows = []
	for element in results:
		row = parseElement(element)
		if row is not None and len(row) > 0:
			rows.append(row)
	rows = validateContent(rows)
	rows = validateContent(rows)
	rows = validateContent(rows)
	return rows


"""
* @def name:		validateContent(rows)
* @description:		This function returns a list of search results.
* @related issues:	Charity-002
* @param:			string keywords
* @param:			integer limit
* @return:			list rows
* @author:			Don Hsieh
* @since:			02/24/2016
* @last modified:	02/26/2016
* @called by:		main
*					 in charity/python/search.py
"""
def validateContent(rows):
	for i, row in enumerate(rows):
		if len(row) < 25:
			print len(row)
			print 'row =', row
			url = row[-1]
			print 'url =', url
			details = getDatailPageContent(url)
			if details is not None and len(details) > 0:
				row.extend(details)
				print 'details =', details
				print 'row =', row
				rows[i] = row
	return rows

"""
* @def name:		getNow(format=None)
* @description:		This function returns a string of time of now.
* @related issues:	Charity-002
* @param:			string format=None
* @return:			string now
* @author:			Don Hsieh
* @since:			02/24/2016
* @last modified:	02/24/2016
* @called by:		def writeXls(xls, keywords, rows)
*					 in charity/python/search.py
"""
def getNow(format=None):
	#if format is None: format = '%Y/%m/%d %a %H:%M:%S'
	if format is None: format = '%Y-%m-%d %H:%M:%S'
	now = datetime.now().strftime(format)
	return now


"""
* @def name:		writeXls(xls, keywords, rows)
* @description:		This function exports data from table to xls file.
* @related issues:	Charity-002
* @param:			string xls
* @param:			string keywords
* @param:			list rows
* @return:			void
* @author:			Don Hsieh
* @since:			02/24/2016
* @last modified:	02/26/2016
* @called by:		main
*					 in charity/python/search.py
"""
def writeTitles(fileName):
	title = u'標的方	買方	交易金額	所屬行業	宣佈時間	詳情	交易類型	交易方式	是否跨境併購	是否關聯交易	交易態度	交易狀態	交易宣佈時間	交易結束時間	交易金額	企業估值(US$M)	支付方式	行業分類	標的企業	買方企業	投資銀行	律師事務所	會計事務所	資產評估公司	交易描述'
	path = os.path.dirname(os.path.realpath(__file__))
	fileName = os.path.join(path, fileName)
	with codecs.open(fileName, "w", "utf-8") as temp:
		temp.write(title)


"""
* @def name:		writeXls(xls, keywords, rows)
* @description:		This function exports data from table to xls file.
* @related issues:	Charity-002
* @param:			string xls
* @param:			string keywords
* @param:			list rows
* @return:			void
* @author:			Don Hsieh
* @since:			02/24/2016
* @last modified:	02/26/2016
* @called by:		main
*					 in charity/python/search.py
"""
def writeTxt(fileName, rows):
	lines = []
	for row in rows:
		line = '\t'.join(row)
		if len(line) > 3:
			lines.append(line)
	content = '\n'.join(lines).strip()
	content = '\n' + content
	print 'content =', content
	print 'len(content) =', len(content)

	# with codecs.open("merge.txt", "w", "utf-8-sig") as temp:
	with codecs.open(fileName, "a", "utf-8") as temp:
		temp.write(content)

path = os.path.dirname(os.path.realpath(__file__))
s = 'merge_1_to_75_' + getNow().replace(' ', '_').replace(':', '')
s += '.csv'
fileName = os.path.join(path, s)
out = open(fileName, 'wb')
# fields = ['標的方', '買方', '交易金額', '所屬行業', '宣佈時間', '詳情', '交易類型', '交易方式', '是否跨境併購', '是否關聯交易', '交易態度', '交易狀態', '交易宣佈時間', '交易結束時間', '交易金額', '企業估值(US$M)', '支付方式', '行業分類', '標的企業', '買方企業', '投資銀行', '律師事務所', '會計事務所', '資產評估公司', '交易描述']
writer = csv.writer(out)

path = os.path.dirname(os.path.realpath(__file__))
# fileName = os.path.join(path, 'merge_21_to_21_2016-02-20_223749.txt')
fileName = os.path.join(path, 'merge_1_to_75_2016-02-20_233051.txt')
with open(fileName) as f:
	lines = f.readlines()
	for line in lines:
		row = line.strip().split('\t')
		if len(row) == 25:
			row[-1] = row[-1].replace('<br>', '\n')
			writer.writerow(row)

out.close()
raise

start = 1
offset = 65
end = start + offset

s = 'merge_' + str(start) + '_to_' + str(end-1) + '_' + getNow().replace(' ', '_').replace(':', '')
s += '.txt'
print s
path = os.path.dirname(os.path.realpath(__file__))
fileName = os.path.join(path, s)
# results = []
writeTitles(fileName)
for pageNumber in range(start, end):
	print '\n' + 'pageNumber =', pageNumber
	print getNow()
	content = getPageContent(pageNumber)
	results = []
	results.append([str(pageNumber), getNow()])
	results.extend(content)
	writeTxt(fileName, results)

print("Done")