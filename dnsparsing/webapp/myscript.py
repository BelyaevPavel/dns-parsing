from lxml import html, etree
import requests

def hello():
    page = requests.get('http://www.dns-shop.ru/catalog/17a89b1a16404e77/tyunery-dlya-kompyutera/')
    tree=etree.HTML(page.content, parser=etree.HTMLParser(encoding='utf-8'))
    products= tree.xpath('//div[@class="product"]')
    product = tree.xpath('//div[@class="product"]//div[@class="item-name"]/a[@class="ec-price-item-link"]/text()')
    prices = tree.xpath('//div[@class="product"]//div[@class="item-price"]//span[@data-product-param="price"]/text()')
    refs = tree.xpath('//div[@class="product"]//div[@class="item-name"]/a/@href')
    a=[[0]*3 for i in range(len(product))]
    for i in range(len(product)):
        a[i][0]=product[i]
        a[i][1]=prices[i]
        a[i][2]='www.dns-shop.ru'+refs[i]

#    for i in range(len(product)):
#        print a[i][0],a[i][1],a[i][2]
    return a
