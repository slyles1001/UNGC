from lxml import html
import requests


link = '/Users/ducttapecreator/Desktop/TA-list-pages/TA-list-page'
for i in range(1):#,181):
	cur_link = link + str(i)
	page = requests.get(cur_link)
	tree = html.fromstring(page.content, base_url, parser)
	name = tree.xpath('//th[@class="name"]/text()')
	typ = tree.xpath('//tr[@class=type"]/text()')
	print(name)