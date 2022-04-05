import json
import re
from math import floor
from random import randint
from time import time, strftime, strptime

from lxml import html

from .extractor import Extractor


class Bing(Extractor):

    def today(self):
        result = self.get('https://cn.bing.com/')
        dom = html.fromstring(result.content)
        return {
            'date': strftime('%Y%m%d', strptime(re.findall(r'"Lad":"(\d{4}-\d{2}-\d{2})', result.content.decode()).pop(), '%Y-%m-%d')),
            'url': dom.xpath('//link[@id="preloadBg"]/@href').pop(),
            'copyright': '{} ({})'.format(dom.xpath('//div[@class="musCardCont"]//text()')[1].encode('latin-1').decode('utf-8'),
                                          dom.xpath('//div[@class="musCardCont"]//text()')[2].encode('latin-1').decode('utf-8')),
            'location': 'pic/' + re.findall(r'id=(.+)&', dom.xpath('//link[@id="preloadBg"]/@href').pop()).pop()
        }

    def specify(self, day):
        result = self.get(f'https://cn.bing.com/HPImageArchive.aspx?format=js&idx={day}&n=1&nc={floor(time() * 1000)}&pid=hp')
        response = json.loads(result.content).get('images').pop()
        return {
            'date': response.get('enddate'),
            'url': 'https://s.cn.bing.net' + response.get('url'),
            'copyright': response.get('copyright'),
            'location': 'pic/' + re.findall(r'id=(.+)&', response.get('url')).pop()
        }

    def random(self):
        number = randint(0, 1000)
        if number == 0:
            return self.today()
        else:
            return self.specify(number)
