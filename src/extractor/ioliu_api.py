import json
import re
from datetime import datetime

from lxml import html

from .extractor import Extractor


class IoLiuAPI(Extractor):

    def today(self):
        return self.specify(0)

    def specify(self, day):
        result = self.get(f'https://bing.ioliu.cn/v1?d={day}&type=json')
        response = json.loads(result.content).get('data')
        data = {
            'date': response.get('enddate'),
            'url': response.get('url'),
            'location': 'pic/' + re.findall(r'.+/(.+)', response.get('url')).pop()
        }
        delta = (datetime.now() - datetime.strptime(data.get('date'), '%Y%m%d')).days
        div, mod = divmod(delta, 12)
        result = self.get(f'https://bing.ioliu.cn/?p={div + 1}')
        dom = html.fromstring(result.content)
        t = datetime.strftime(datetime.strptime(data.get("date"), "%Y%m%d"), "%Y-%m-%d")
        data['copyright'] = dom.xpath(f'//div[@class="item"]//p[@class="calendar"]/em[@class="t" and text()="{t}"]/ancestor::div[@class="description"]/h3/text()').pop()
        return data

    def random(self):
        result = self.get(f'https://bing.ioliu.cn/v1/rand?type=json')
        response = json.loads(result.content).get('data')
        return {
            'date': response.get('enddate'),
            'url': response.get('url'),
            'copyright': response.get('copyright'),
            'location': 'pic/' + re.findall(r'.+/(.+)\?', response.get('url')).pop()
        }
