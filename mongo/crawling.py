import time
import requests
from requests.adapters import HTTPAdapter
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib3.util.retry import Retry
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# Webdriver headless mode setting
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
# 창 유지 옵션
options.add_experimental_option("detach", True)
# 창 invisible 옵션(디버깅 용, 실제 실행시 켜기)
options.add_argument("disable-gpu")
service = Service(executable_path=r"C:\work\TextCrafters\chromedriver.exe")

# BS4 setting for secondary access
session = requests.Session()
headers = {
    "User-Agent": "user value"}

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])

session.mount('http://', HTTPAdapter(max_retries=retries))

# 검색어
# search = input()
search = "서강대 맛집"
search.replace(" ", "+")
url = "https://m.place.naver.com/restaurant/list?query=" + search

rest_list = []
# 검색어 음식점 개수
# rest_num = input()
rest_num = 50
rev_num = 50

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
driver.implicitly_wait(10)

driver.find_element(By.XPATH, '//*[@id="_place_portal_root"]/div/a').click()
driver.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div').click()

temp = (driver.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[2]/ul')
        .find_elements(By.CLASS_NAME, "UEzoS"))
while len(temp) < rest_num:
    # Page down
    for i in range(10):
        driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div').send_keys(Keys.PAGE_DOWN)
        driver.implicitly_wait(5)
    # try again
    temp = (driver.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[2]/ul')
            .find_elements(By.CLASS_NAME, "UEzoS"))

temp = temp[0:rest_num]

for tem in temp:
    a = tem.find_element(By.TAG_NAME, "a").get_attribute("href")
    rest_url = a.replace("?", "/review?")
    rest_name = (tem.find_element(By.TAG_NAME, "a")).find_element(By.CLASS_NAME, "TYaxT").text
    rest_list.append((rest_name, rest_url))

print(rest_list)

# 식당 페이지 하나씩 순회
for rest in rest_list:
    try:
        # 로딩될 때 까지 최대 10초 대기
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
    except TimeoutException:
        # 실패 시에는 에러메시지로 Time Out 출력
        print('Time Out')

    # scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(2)

    # 음식점 이름  print (디버깅 용)
    print(rest[0])
    try:
        driver.get(rest[1])
        driver.implicitly_wait(3)
    except:
        continue

    # review 개수 조정
    try:
        n = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/h2/span[1]').text
    except:
        # driver.find_element(By.TAG_NAME, 'body').click()
        # Page down
        # scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # try again
        n = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/h2/span[1]').text

    all_rev = n.replace(",", "")
    if int(all_rev) < rev_num:
        rev_num = n

    temp = (driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[1]/ul')
            .find_elements(By.CLASS_NAME, "YeINN"))
    try:
        while len(temp) < rev_num:
            # 더보기 클릭
            try:
                # 로딩될 때 까지 최대 10초 대기
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a'))
                )
            except TimeoutException:
                # 실패 시에는 에러메시지로 Time Out 출력
                print('Time Out')
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a').click()
            time.sleep(0.4)
            # try again
            temp = (driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[1]/ul')
                    .find_elements(By.CLASS_NAME, "YeINN"))
    except Exception as e:
        print('finish')

    reviews = temp[0:rev_num]

    # review 순회
    j = 0
    time.sleep(2)
    for rev in reviews:
        print(j)
        try:
            review = (rev.find_element(By.CLASS_NAME, "ZZ4OK")).find_element(By.CLASS_NAME, "zPfVt").text
        except NoSuchElementException:
            print(" ")
        else:
            print(review)
        j = j + 1

        ###########################
        ## 대표 키워드 추출 알고리즘 ##
        ###########################

        ## DB에 식당 이름(rest[0])과 대표 키워드 저장
