import json

import requests
from requests import RequestException

global end_cursor
global hasNext
end_cursor = ''
hasNext = True


def get_page_index_ajax(end_cursor):
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://juejin.im',
        'Referer': 'https://juejin.im',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Agent': 'Juejin/Web',
        'accept': '*/*',
        'X - Legacy - Device - Id': '',
        'X - Legacy - Token': '',
        'X - Legacy - Uid': ''
    }
    params = {
        "operationName": "",
        "query": "",
        "variables": {
            "first": 20,
            "after": end_cursor,
            "order": "POPULAR"
        },
        "extensions": {
            "query": {
                "id": "21207e9ddb1de777adeaca7a2fb38030"
            }
        }
    }

    try:
        response = requests.post('https://web-api.juejin.im/query', headers=headers, data=json.dumps(params))
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_page_url(html):
    j = json.loads(html)
    items = j.get('data').get('articleFeed').get('items')
    page_info = items.get('pageInfo')
    if page_info.get('hasNextPage'):
        global end_cursor
        end_cursor = page_info['endCursor']
    else:
        global hasNext
        hasNext = False

    # 遍历20条信息

    for node in items.get('edges'):
        print(node['node']['originalUrl'])


def main():
    global hasNext
    while hasNext: #如果有下一页就一直循环这个
        global end_cursor
        html = get_page_index_ajax(end_cursor)
        get_page_url(html)
        print(end_cursor)




if __name__ == "__main__":
    main()
