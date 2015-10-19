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
#
# for Mac
# brew install python3
# sudo pip3 install requests xlsxwriter beautifulsoup4 python-dateutil pdfkit
# pip install --upgrade lxml
## sudo port install py27-lxml
#
# sudo apt-get install wkhtmltopdf
# https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
# sudo pip uninstall wkhtmltopdf
# sudo apt-get install python3 python3-pip
# sudo mv /usr/bin/python /usr/bin/python_2.7; sudo ln -fs /usr/bin/python3.4 /usr/bin/python

# https://xlsxwriter.readthedocs.org/
# https://developers.google.com/custom-search/docs/xml_results#WebSearch_Request_Format
import requests
from bs4 import BeautifulSoup, Comment
import urllib.parse		# Python 3
# import urllib		# Python 2
# from urlparse import urlparse		# Python 2
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
import zipfile

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
		# keywords[key] = urlparse(word)

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
* @def name:		shortenUrl(url)
* @description:		This function shortens an URL.
* @related issues:	Charity-001
* @param:			string url
* @return:			string urlShorten
* @author:			Don Hsieh
* @since:			10/10/2015
* @last modified:	10/10/2015
* @called by:		def getUrlInfo(title, description, url)
*					 in charity/python/search.py
"""
def shortenUrl(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
		"Accept-Encoding": "gzip, deflate",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive"
	}
	try:
		url = 'http://tinyurl.com/api-create.php?url=' + url
		r = requests.get(url, headers=headers, timeout=10)
		urlShorten = r.text
		return urlShorten
	except requests.exceptions.Timeout as e:
		# Maybe set up for a retry, or continue in a retry loop
		print('Exception - Timeout: ', e)
		# raise
		return None
	except requests.exceptions.ConnectionError as e:
		print('Exception - ConnectionError: ', e)
		# raise
		return None
	except requests.exceptions.HTTPError as e:
		print('Exception - HTTPError: ', e)
		raise
	except requests.exceptions.TooManyRedirects as e:
		print('Exception - TooManyRedirects: ', e)
		raise
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
		raise

"""
* @def name:		getUrlInfo(title, description, url)
* @description:		This function returns statusCode, contentLength,
*					 contentType, and contentDisposition of an URL.
* @related issues:	Charity-001
* @param:			string title
* @param:			string description
* @param:			string url
* @return:			list row
* @author:			Don Hsieh
* @since:			10/09/2015
* @last modified:	10/10/2015
* @called by:		def getCiteUrl(key, element)
*					 in charity/python/search.py
"""
def getUrlInfo(title, description, url):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
		"Accept-Encoding": "gzip, deflate",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive"
	}
	try:
		r = requests.get(url, headers=headers, timeout=10, verify=False)
		# http://docs.python-requests.org/en/latest/user/advanced/
		# Requests can also ignore verifying the SSL certificate if you set verify to False.
		# >>> requests.get('https://kennethreitz.com', verify=False)
		# <Response [200]>
		if (len(r.history) > 1):
			print('r.history =', r.history)
			url = r.history[-1].headers['Location'].strip('/')
		if len(url) > 100:
			url = shortenUrl(url)
			print(url)

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
		row = [title, description, url, statusCode
		, contentLength, contentType, contentDisposition]
		return row
	except requests.exceptions.Timeout as e:
		# Maybe set up for a retry, or continue in a retry loop
		print('Exception - Timeout: ', e)
		# raise
		return None
	except requests.exceptions.ConnectionError as e:
		print('Exception - ConnectionError: ', e)
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
		raise

"""
* @def name:		getCiteUrl(key, element)
* @description:		This function returns cite URL of a Google
*					 search result.
* @related issues:	Charity-001
* @param:			integer key
* @param:			bs4.element.Tag element
* @return:			tuple title, url
* @author:			Don Hsieh
* @since:			10/10/2015
* @last modified:	10/10/2015
* @called by:		getSearchResult(keywords, limit)
*					 in charity/python/search.py
"""
def getCiteUrl(key, element):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
		"Accept-Encoding": "gzip, deflate",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive"
	}
	title = None
	description = None
	url = None
	statusCode = None
	contentLength = None
	contentType = None
	contentDisposition = None

	if element.find('span', {'class': 'st'}) is not None:
		description = element.find('span', {'class': 'st'}).getText().replace('\n', '').strip()
	elif element.find('div', {'class': 's'}) is not None:
		description = element.find('div', {'class': 's'}).getText().replace('\n', '').strip()
	else:
		print("element =")
		print(element)

	if element.find('cite') is not None:
		title = element.find('a').getText().strip()
		citeUrl = element.find('cite').getText().strip()
		print('\n' + str(key) + '\t' + title)
		print('citeUrl =' + '\t' + citeUrl)
		titleUrl = element.find('a')['href'].strip()
		if '...' in citeUrl or '›' in citeUrl:
			# <cite class="_Rm bc">big.hi138.com › 經濟學論文 › 新經濟學論文</cite>
			print('titleUrl =' + '\t' + titleUrl)
			if titleUrl[0] == '/':
				url = 'https://www.google.com.tw' + titleUrl
			else: url = titleUrl
			print('url =' + '\t' + url)
		else: url = citeUrl
		url = url.lower()
		if 'http' not in url: url = 'http://' + url
		print(description)
		row = getUrlInfo(title, description, url)
		return row
	else: return None

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
	urlQuery = getQueryUrl(keywords)
	start = 0
	num = 0
	count = limit
	rows = []
	key = 1
	while count > 0:
		if count > 20:
			num = 20
		else: num = count
		urlRequest = urlQuery + '&start=' + str(start) + '&num=' + str(num)
		print(urlRequest)
		r = requests.get(urlRequest, headers=headers, timeout=10)
		# soup = BeautifulSoup(r.text)	# Python2
		soup = BeautifulSoup(r.text, "lxml")
		results = soup.findAll('div', {'class': 'g'})
		for element in results:
			row = getCiteUrl(key, element)
			if row is not None:
				rows.append(row)
				key += 1
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
	xls += '_' + str(cntRows) + '_' + date + '.xlsx'
	fields = ['Title', 'Description', 'URL', 'status code', 
	'content-length', 'content-type', 'content-disposition'
	, 'file size']
	workbook = xlsxwriter.Workbook(xls)
	# worksheet = workbook.add_worksheet(keywords)
	sheet = workbook.add_worksheet(keywords)
	# Widen the first column to make the text clearer.
	sheet.set_column('A:A', 50)
	sheet.set_column('B:B', 130)
	sheet.set_column('F:F', 20)

	col = 0
	for field in fields:
		# print(field)
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
	workbook.close()
	return xls.split('/')[-1].split('.')[0]

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
* @def name:		parseContentDisposition(contentDisposition)
* @description:		This function gets file name from
*					 'content-disposition' header.
* @related issues:	Charity-001
* @param:			string contentDisposition
* @return:			string fileName
* @author:			Don Hsieh
* @since:			10/09/2015
* @last modified:	10/09/2015
* @called by:		def getLocalFileName(row, key, folder)
*					 in charity/python/search.py
"""
def parseContentDisposition(contentDisposition):
	fileName = contentDisposition.split('=')[-1].split('"')[-1]
	fileName = fileName.split("'")[-1]
	fileName = fileName.replace('"', '').replace("'", '')
	fileName = fileName.replace(';', '')
	# fileName = fileName.replace('(', '').replace(')', '')
	return fileName

"""
* @def name:		getFileExtension(row, fileName)
* @description:		This function returns extension of the file.
* @related issues:	Charity-001
* @param:			list row
* @param:			string fileName
* @return:			string extension
* @author:			Don Hsieh
* @since:			10/09/2015
* @last modified:	10/09/2015
* @called by:		def getLocalFileName(row, key, folder)
*					 in charity/python/search.py
"""
def getFileExtension(row, fileName):
	extension = None
	extensions = ['htm', 'html', 'pdf', 'doc', 'docx', 'txt'
	, 'ppt', 'pptx' , 'xls', 'xlsx']
	if '.' in fileName:
		extension = fileName.split('.')[-1].lower()
		if extension not in extensions:
			extension = None
	if extension is None and row[5] is not None:
		contentType = row[5].lower()
		if 'application/pdf' in contentType:
			extension = 'pdf'
		elif 'application/vnd.ms-powerpoint' in contentType:
			extension = 'ppt'
		elif 'application/msword' in contentType:
			extension = 'doc'
		elif 'text/html' in contentType:
			extension = 'html'
	return extension

"""
* @def name:		getLocalFileName(row, key, folder)
* @description:		This function decides name of downloaded file.
* @related issues:	Charity-001
* @param:			list row
* @param:			int key
* @param:			string folder
* @return:			string localFileName
* @author:			Don Hsieh
* @since:			07/27/2015
* @last modified:	07/27/2015
* @called by:		def getFiles(folder, results)
*					 in charity/python/search.py
"""
def getLocalFileName(row, key, folder):
	localFileName = None
	contentDisposition = row[6]
	if contentDisposition is not None:
		localFileName = parseContentDisposition(contentDisposition)
		if '.' in localFileName:
			extension = localFileName.split('.')[-1]
			extensions = ['htm', 'html', 'pdf', 'doc', 'docx', 'txt'
			, 'ppt', 'pptx' , 'xls', 'xlsx']
			if extension not in extensions:
				localFileName = None

	if localFileName is None:
		url = row[2]
		print(url)
		localFileName = urllib.parse.unquote(url.split('/')[-1]).split('?')[0].replace(' ', '-')
		extension = getFileExtension(row, localFileName)

		title = row[0]
		name = title.split(' ')[0]
		name = name.replace('#', '').replace('"', '').replace('>', '')
		name = name.replace('@', '').replace('[', '').replace(']', '')
		name = name.split('(')[0].split(u'（')[0].split('/')[0].split('｜')[0]
		name = name.split('!')[0].split('?')[0].split('.')[0].split('*')[0]
		name = name.split('|')[0].split('！')[0].split('.')[0].split('*')[0]
		print(name)
		print(url)

		if name != localFileName.split('.')[0]:
			if len(name) > 3:
				localFileName = name + '_' + localFileName
		localFileName = str(key) + '_' + localFileName
		localFileName = localFileName.replace('--', '-')
		localFileName = localFileName.replace('__', '_')
		localFileName = localFileName.replace('/', '')
		# localFileName = localFileName.replace('(', '')
		# localFileName = localFileName.replace(')', '')
		localFileName = os.path.join(folder, localFileName)
		if localFileName.endswith('/'):
			localFileName = localFileName[:-1]
		# if "." not in localFileName:
		# 	localFileName += '.html'
		localFileName = localFileName.split('.')[0]
		if extension is not None:
			localFileName += '.' + extension
		localFileName = localFileName.replace('..', '.')
		localFileName = localFileName.replace('_.', '.')
		localFileName = localFileName.replace('».', '.')
		localFileName = localFileName.replace('~', '')
		# localFileName = localFileName.replace('//', '')
	# print(localFileName)
	return localFileName

"""
* @def name:		getFiles(folder, results, limit)
* @description:		This function downloads files to given folder.
* @related issues:	Charity-001
* @param:			string folder
* @param:			list results
* @param:			integer limit
* @return:			void
* @author:			Don Hsieh
* @since:			07/24/2015
* @last modified:	07/26/2015
* @called by:		main
*					 in charity/python/search.py
"""
def getFiles(folder, results, limit):
	rows = []
	print(folder)
	if not os.path.exists(folder):
		os.makedirs(folder)

	# command = 'wget -d -c -t 7'
	# command = 'wget -d -c -t 7 --restrict-file-names=nocontrol'
	command = 'wget -d -c -t 6 --restrict-file-names=nocontrol'
	# command += ' --remote-encoding=utf-8'
	command += ' --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36"'
	command += ' --header="Referer: http://www.google.com/"'
	command += ' --header="Accept-Encoding: compress, gzip"'
	# command += ' --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"'
	# command += ' --header="Accept-Language: en-US,en;q=0.5"'

	key = 1
	# for key, result in enumerate(results):
	for result in results:
		statusCode = result[3]
		if statusCode is not None and statusCode < 400 and key <= limit:
			title = result[0]
			url = result[2]
			localFileName = getLocalFileName(result, key, folder)
			if localFileName is not None and len(localFileName) > 3:
				if '.htm' not in localFileName:
					wgetCommand = command + ' -O "' + localFileName + '"'
					wgetCommand += ' "' + url + '"'
					os.system(wgetCommand)
					# wget -d --header="User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11" --header="Referer: http://xmodulo.com/" --header="Accept-Encoding: compress, gzip" http://www.google.com/
					# os.system('wget -O example.html http://www.electrictoolbox.com/wget-save-different-filename/')
				else:
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
						print('Exception - Timeout: ', e)
					except requests.exceptions.ConnectionError as e:
						print('Exception - ConnectionError: ', e)
					except requests.exceptions.HTTPError as e:
						print('Exception - HTTPError: ', e)
					except requests.exceptions.TooManyRedirects as e:
						print('Exception - TooManyRedirects: ', e)
					except requests.exceptions.URLRequired as e:
						print('Exception - Valid URL Required: ', e)
					except requests.exceptions.RequestException as e:
						print('Exception (Ambiguous requests exception): ', e)
					except IOError as e:
						print("I/O error: ", e)
					except:
						print("Unexpected error:", sys.exc_info()[0])
				print('localFileName =', localFileName)
				fileSize = '0 byte'
				try:
					fileSize = os.path.getsize(localFileName)
					print('fileSize =', fileSize)
					if fileSize < 2000:
						os.remove(localFileName)
					if fileSize > 1000000:
						fileSize = round(fileSize / 1000000, 1)
						if fileSize >= 100:
							fileSize = int(fileSize)
						fileSize = str(fileSize) + ' MB'
					elif fileSize > 1000:
						fileSize = round(fileSize / 1000, 1)
						if fileSize >= 100:
							fileSize = int(fileSize)
						fileSize = str(fileSize) + ' KB'
					else:
						fileSize = str(fileSize) + ' byte'
				except:
					print('Error: ', sys.exc_info()[0])
				row = result
				row.append(fileSize)
				print('row =', row)
				rows.append(row)
				key += 1
	return rows

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
		localFileName = str(key+1) + '.pdf'
		print(title)
		print(url)
		print(localFileName)
		pdfkit.from_url(url, localFileName, options=options)
		# pdfkit.from_url(['google.com', 'yandex.ru', 'engadget.com'], 'out.pdf')

"""
* @def name:		zip(src, dst)
* @description:		This function zips a directory.
* @related issues:	Charity-001
* @param:			string src
* @param:			string dst
* @return:			void
* @author:			Don Hsieh
* @since:			10/12/2015
* @last modified:	10/12/2015
* @called by:		main
*					 in charity/python/search.py
"""
def zip(src, dst):
	zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
	abs_src = os.path.abspath(src)
	for dirname, subdirs, files in os.walk(src):
		print("files =", files)
		for filename in files:
			absname = os.path.abspath(os.path.join(dirname, filename))
			arcname = absname[len(abs_src) + 1:]
			s = 'zipping ' + os.path.join(dirname, filename)
			s += ' as ' + arcname
			print(s)
			zf.write(absname, arcname)
	zf.close()

# dirFiles = "第 3 組"
# # dirFiles = "第 4 組"
# dirFiles = "第 6 組"
# # dirFiles = "第 2 組"
# # ## dirFiles = "第 1 組"
#path = os.path.dirname(os.path.realpath(__file__))
# src = os.path.join(path, dirFiles)
# dst = os.path.join(path, dirFiles)
# delFile = os.path.join(src, ".DS_Store")
# if os.path.exists(delFile):
# 	os.remove(delFile)
# zip(src, dst)
# raise

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36",
	"Accept-Encoding": "gzip, deflate",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.5",
	"Connection": "keep-alive"
}

dirFiles = "第 3 組"
keywords = '弱勢家庭'

path = os.path.dirname(os.path.realpath(__file__))
xls = os.path.join(path, keywords)

# limit = 1
# limit = 5
# limit = 10
limit = 100
if limit >= 100:
	results = getSearchResult(keywords, limit + 20)
elif limit >= 50:
	results = getSearchResult(keywords, limit + 10)
elif limit >= 30:
	results = getSearchResult(keywords, limit + 5)
else:
	results = getSearchResult(keywords, limit)
# writeXls(xls, keywords, results)
# raise
folderName = 'files_' + keywords.replace(' ', '_') + '_' + str(len(results)) + '_' + getNow('%y%m%d_%H%M')
folder = os.path.join(path, folderName)
# exportHtmlToPdf(results, folder)

# getFiles(folder, results)
results = getFiles(folder, results, limit)
xlsName = writeXls(xls, keywords, results)
folderName = 'files_' + xlsName
folderUpdated = os.path.join(path, folderName)
# print('xlsName =', xlsName)
# print('folderName =', folderName)
# print('folder =', folder)
# print('folderUpdated =', folderUpdated)
os.rename(folder, folderUpdated)

# zip dir into a zipped file
src = os.path.join(path, dirFiles)
dst = os.path.join(path, dirFiles)
delFile = os.path.join(src, ".DS_Store")
if os.path.exists(delFile):
	os.remove(delFile)
zip(src, dst)

print("Done")