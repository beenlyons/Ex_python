import re
import requests
'''抓取网页，获取图片，保存到本地'''

url = "https://www.imooc.com/course/list?c=python"
r = requests.get(url)
html = r.text

pa = re.compile(r'''src="(.+\.jpg)"''')
urls = pa.findall(html)
urls = map(lambda x:"http:" + x, urls)
i = 1
for uri in urls:
    with open(r"./image/" +str(i)+".jpg", "wb") as f:
        req = requests.get(uri)
        f.write(req.content)
        i +=1
