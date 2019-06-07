import json
from multiprocessing.pool import Pool
import pymysql
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)

    # print(items)
    for item in items:
        yield [
            item[0],
            item[1],
            item[2],item[3],item[4],item[5], item[6]


        ]
        # yield {
        #     'index':item[0],
        #     'image': item[1],
        #     'title': item[2],
        #     'actor': item[3].strip()[3:],
        #     'time': item[4].strip()[5:],
        #     'score': item[5]+ item[6],
        # }
def write_to_file(content):
    with open('C:/Users/zhangpingyang/Desktop/result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def write_to_mysql(item):
    conn = pymysql.connect(
        host='localhost',
    user ="root", password ="root",
    database ="python",
    charset ="utf8")
    cursor = conn.cursor()
    sql = "INSERT INTO `python`.`maoyantop100`(`index`, `image`, `title`, `actor`, `time`, `score`)" \
          " VALUES ('"+str(item[0])+"', '"+str(item[1])+"', '"+str(item[2])+"', '"+str(item[3].strip()[3:])+"', '"\
          +str(item[4].strip()[5:])+"', '"+str(item[5] + item[6])+"');"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # for item in parse_one_page(html):
    #     print(item)
    #     # write_to_file(item)
    for item in parse_one_page(html):
        write_to_mysql(item)
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    # pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])