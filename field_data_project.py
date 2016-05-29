import os
import sys
import re
import requests
import csv
from datetime import datetime
from functools import reduce
from bs4 import BeautifulSoup


PATH = os.getcwd() + "/"
dw_path = PATH + "dw_field_data/"

YEAR=2016
TODAY = datetime.date(datetime.now())
print("Today is {}".format(TODAY))
date_format = "%a %b %d %Y"
date_format_2 = "%b %d %Y"
LASTTIME="May 27 2016"
LT_ST = datetime.date(datetime.strptime(LASTTIME,date_format_2))
print("Last time you scraped is {}".format(LT_ST))
URL="http://us.cnn.com"
url_list = ["http://us.cnn.com","http://edition.cnn.com"]
title_list = {}

def get_cnn_news(url):
	try:
		page = BeautifulSoup(requests.get(url).text, "lxml")
	except:
		print("Some errors occur when retrieving the page of cnn news!")
		sys.exit(0)
	title = page.find('div',"nav--plain-header",id="nav__plain-header")
	title_content = title.find('div','nav__container').find('div','nav-menu-links')
	for i in title_content.children:
		if re.search("//",i["href"]) and i.text not in title_list:
			title_list[i.text] = "http:" + i["href"]
		elif i.text not in title_list:
			title_list[i.text]= url + i["href"]
		else:
			continue		
	print(title_list)
	#del title_list['Features']
	#del title_list['Money']
	#del title_list['Regions']
	#del title_list['U.S. Politics']
	print("Lets scrape section by section")
	# for element in sorted(title_list.keys()):
	# 	print("Here we have {}".format(element))
	# 	print(title_list[element])
	# 	indexes = get_cnn_news_topic(title_list[element],element,URL)
	# 	#parse all story here.
	# 	#print(indexes)
	# 	# stories = parse_cnn_story(indexes,URL)
	# 	# write_to_csv(stories)
	# 	# sys.exit(0)

def get_cnn_news_topic(url,keyword,URL):
    	try:
    		page = BeautifulSoup(requests.get(url).text,"lxml")
    	except:
    		print("We found error when get page from {}".format(url))
    		return
    	result = []
    	index = url.split("/")[-1]+"-zone-"
    	#print(index)
    	num=2
    	if keyword== "Tech":
    		num=1
    	ind =index+str(num)
    	# if keyword=="Travel":
    	# 	ind = "intl_"+ind
    	chunk = page.body.find("section",id=ind)
    	# if url =='http://www.cnn.com/politics':
    	# 	print(chunk)
    	# 	print(index+str(num))
    	# 	print(page.body.find_all("section"))
    	# #just top story here
    	#k = len(chunk.find_all("div",class_=re.compile("column zn__column--idx-")))
    	#print(k)
    	try:
    		for j in range(7):
    			for entry in chunk.find("div","column zn__column--idx-" + str(j)).ul.find_all("article"):
    				pre_link= entry["data-vr-contentbox"]
    				if re.search("http",pre_link):
    					link = pre_link
    				else:
    					link =URL + entry["data-vr-contentbox"]
    				result.append(link)
    	except:
    		print("Stop here {}".format(j))
    	print(result)
    	return result
	

def parse_cnn_story(indexes,URL):
		result = {}
		for link in indexes:
			if not re.search(".html",link):
				continue
			try:
				page = BeautifulSoup(requests.get(link).text,"lxml")
			except:
				print("We found some error while parsing stories")
				continue
			if re.search("money.cnn.com",link):
				Body= page.body.find('main','container js-social-anchor-start')
				title_list= Body.find('header').find_all('div',"row")
				pure_title = title_list[0].find("h1","article-title").text
				time =title_list[1].find("span","cnnDateStamp").text
				if not check(time):
					continue
				title= pure_title + " " + time
				content = Body.find("section", "column").find("div",id="storytext").get_text()
				result[title]=content	
			elif re.search("edition.cnn.com",link) or re.search("us.cnn.com",link):
				#print(page.body.find('div','pg-right-rail-tall pg-wrapper '))
				print("we are scraping {}".format(link))
				#print(page.body.find('div',re.compile("pg-right-rail-tall pg-.*")))
				try:
					#Body= page.body.find('div',"pg-right-rail-tall pg-wrapper ").article.find('div','l-container')
					Body= page.body.select("div.pg-right-rail-tall.pg-wrapper")[0].article.find('div','l-container')
				except:
					print("We fail to parse {}".format(link))
					continue
				#print(Body.prettify()) 
				pure_title= Body.find('h1','pg-headline').text
				time = Body.find('div','metadata').find('p',"update-time").text
				print(time)
				if not check(time):
					continue
				title= pure_title + " " + time
				content_temp= Body.find("section",id= "body-text").find("div",'l-container').find_all(attrs={'class':"zn-body__paragraph"})
				content_temp[0]=content_temp[0].get_text()	
				content = reduce(content_gen,content_temp)
				result[title]=content
			else:
			    print("We dump one {}".format(link))
		return result

def write_to_csv(field,stories):
	number = len(stories)
	count=0
	for i in stories.keys():
		with open(dw_path+field+":"+i+".txt",'w') as csvfile:
			csvfile.write(stories[i])
		count+=1
		print("write the {} story".format(count))

def check(date):
	timeline =date.split(",")
	for i,j in enumerate(timeline):
		if re.search(str(YEAR),j):
			break
	#timeline = ("".join(date.split(",")[-2:])).strip(" ")
	timeline= (re.sub("  "," ",timeline[i-1]+" " +str(YEAR))).strip(" ")
	try:
		target = datetime.date(datetime.strptime(timeline, date_format))
	except:
		target = datetime.date(datetime.strptime(timeline, date_format_2))
	print(target>LT_ST)
	return(target>LT_ST)

def content_gen(x,y):
	return x +"\n"+ y.get_text()


if __name__ == "__main__":
	for entry in url_list:
		get_cnn_news(entry)
	del title_list['Video']
	for element in sorted(title_list.keys()):
		print("Here we have {}".format(element))
		print(title_list[element])
		indexes = get_cnn_news_topic(title_list[element],element,URL)
		print("----------------------------------------------")
		#parse all story here.
		stories = parse_cnn_story(indexes,URL)
		#sys.exit(1)
		write_to_csv(element,stories)
	# a = get_cnn_news_topic("http://us.cnn.com/politics","Politics","http://edition.cnn.com")

