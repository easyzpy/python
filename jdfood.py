import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
def search():
    try:

        browser.get('https:www.jd.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))
        )
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[clstag="h|keycount|head|search_c"]'))
        )
        input.send_keys('美食')
        submit.click()
        time.sleep(3)
        # 逐渐滚动浏览器窗口，令ajax逐渐加载
        for i in range(0, 1):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            i += 1
            time.sleep(2)
        #获取页面总页数
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b'))
        )
        # print(total.text)
        return total.text
    except TimeoutException:
        return search()
def next_page(page_number):
    
def main():
    total = search()
    total = int(total)
    print(total)

if __name__ == '__main__':
    main()
