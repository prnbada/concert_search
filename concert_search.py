# This is a sample Python script.
import json
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import time
import os
import sys
import urllib.request

regionList = ["강남","강동","강릉","강북","강서","강진","강화","거제","거창","경산","경주","계룡","계양","고령","고성","고양","고창","고흥","곡성","공주","과천","관악","광명","광산","광양","광주","광진","괴산","구례","구로","구리","구미","군산","군위","군포","금산","금정","금천","기장","김제","김천","김포","김해","나주","남구","남동","남양","남원","남해","노원","논산","단양","달서","달성","담양","당진","대덕","도봉","동구","동대문","동두천","동래","동작","동해","마포","목포","무안","무주","문경","미추홀","밀양","보령","보성","보은","봉화","부산진","부안","부여","부천","부평","북구","사상","사천","사하","산청","삼척","상주","서구","서대문","서산","서천","서초","성남","성동","성북","성주","속초","송파","수성","수영","수원","순창","순천","시흥","신안","아산","안동","안산","안성","안양","양구","양산","양양","양주","양천","양평","여수","여주","연수","연제","연천","영광","영덕","영도","영동","영등포","영암","영양","영월","영주","영천","예산","예천","오산","옥천","옹진","완도","완주","용산","용인","울릉","울주","울진","원주","유성","은평","음성","의령","의성","의왕","의정부","이천","익산","인제","임실","장성","장수","장흥","전주","정선","정읍","제천","종로","중구","중랑","증평","진도","진안","진주","진천","창녕","창원","천안","철원","청도","청송","청양","청주","춘천","충주","칠곡","태백","태안","통영","파주","평창","평택","포천","포항","하남","하동","함안","함양","함평","합천","해남","해운대","홍성","홍천","화성","화순","화천","횡성"]
exceptKeyword = ["후기", "어제", "음란", "레슨", "사망"]
expectKeyword = ["오늘","내일","모레","글피"]
pattern1 = r"\d+월 \d+일"
pattern2 = r"\d+월 \d+일"
resultSearchAll = []

#value = "오늘은 2020년 02월 29일 입니다."
#regex_result = re.search(pattern, value)
#result = regex_result.group()
#print(result)
#exit(0)

# 함수 정의: 검색어 조건에 따른 url 생성
def insta_searching(n_post):
    global regionList
    global exceptKeyword
    global resultSearchAll
    global pattern1
    global pattern2
    global expectKeyword

    source = "insta"

    service = Service(executable_path="/home/prnbada/Work/02.kpopregion/chromedriver")
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.instagram.com')
    time.sleep(3)
    # 인스타그램 로그인을 위한 계정 정보
    email = 'prnbada7@naver.com' # 로그인ID
    input_id = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')
    input_id.clear()
    input_id.send_keys(email)
    password = '12qwasZX!' # 로그인 비번
    input_pw = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input')
    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()
    time.sleep(5)
    print("start searching")
    #word = input("검색어를 입력하세요 : ")
    word = str("공연")
    url = "https://www.instagram.com/explore/tags/" + str(word)

    # 검색 결과 페이지 열기
    driver.get(url)
    time.sleep(10) # 코드 수행 환경에 따라 페이지가 로드되는 데 시간이 더 걸릴수 있어 8초로 변경(2022/01/11)
    # 첫 번째 게시물 클릭
    print("First post")
    first = driver.find_element(By.CSS_SELECTOR, "div._aagw")
    first.click()
    time.sleep(3)

    for n in range(n_post):

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        try:
            content = soup.select('div._a9zs')[0].text
            # content = soup.select('div._a9zs')[0].text
        except:
            content = ''

        #print(content)
        # 해시태그
    #    tags = re.findall(r'#[^\s#,\\]+', content)

        # 작성일자
    #    date = soup.select('time._aaqe')[0]['datetime'][:10]
        for i in range(0, len(regionList)):

            # check region
            regionFound = False
            if regionList[i] in content:
                regionFound = True

            if not regionFound:
                continue

            dateFound = ''
            expectKeywordFound = False
            #for j in range(len(expectKeyword)):
            #    if expectKeyword[j] in content:
            #        expectKeywordFound = True
            #        dateFound = expectKeyword[j]
            #        break

            if not expectKeywordFound:
                regex_result = re.search(pattern1, content)
                if regex_result:
                    expectKeywordFound = True
                    dateFound = regex_result.group()
                else:
                    regex_result = re.search(pattern2, content)
                    if regex_result:
                        expectKeywordFound = True
                        dateFound = regex_result.group()

            if not expectKeywordFound:
                continue

            #exceptKeywordFound = False
            #for j in range(len(exceptKeyword)):
            #    if exceptKeyword[j] in content:
            #        exceptKeywordFound = True
            #        break
            #
            #if exceptKeywordFound:
            #    continue

            if (previousPost == content[:10]):
                continue

            tmpList = [i, regionList[i], content, dateFound, source]
            resultSearchAll.append(tmpList)

            previousPost = content[:10]

        #i = 0
        #resultSearchAll.append([i, regionList[i], "", content, "insta"])

        print("next post")
        right = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh") #"div._abm0")
        right.click()
        time.sleep(3)
        #except:
        #    time.sleep(2)
        #    print("next post")
        #    right = driver.find_element(By.CSS_SELECTOR, "div._abm0")
        #    right.click()
        #    time.sleep(3)

        time.sleep(5)

def naver_searching(isBlog):
    global regionList
    global exceptKeyword
    global resultSearchAll
    global pattern1
    global pattern2
    global expectKeyword

    client_id = "X9aaq3UBkNrPxxAiD58o"
    client_secret = "LENibc2vnj"
    encText = urllib.parse.quote("공연")
    previousPost = ''

    if isBlog :
        urlHead = "https://openapi.naver.com/v1/search/blog?query="
        source = "nblog"
    else:
        urlHead = "https://openapi.naver.com/v1/search/cafearticle.json?query="
        source = "ncafe"

    for n in range(0, 10):
        startCountStr = str(100*n+1)
        url = urlHead + encText + "&display=100&sort=date&start=" + startCountStr # JSON 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            response_body_decoded = response_body.decode('utf-8')
            #print(response_body.decode('utf-8'))

            jsonObject = json.loads(response_body_decoded)
            jsonArray = jsonObject.get("items")
            for list in jsonArray:
                #print(list)
                description = list.get("description")
                for i in range(0, len(regionList)):

                    # check region
                    regionFound = False
                    if regionList[i] in description:
                        regionFound = True

                    if not regionFound :
                        continue

                    dateFound = ''
                    expectKeywordFound = False
                    #for j in range(len(expectKeyword)):
                    #    if expectKeyword[j] in description:
                    #        expectKeywordFound = True
                    #        dateFound = expectKeyword[j]
                    #        break

                    if not expectKeywordFound :
                        regex_result = re.search(pattern1, description)
                        if regex_result:
                            expectKeywordFound = True
                            dateFound = regex_result.group()
                        else:
                            regex_result = re.search(pattern2, description)
                            if regex_result:
                                expectKeywordFound = True
                                dateFound = regex_result.group()


                    if not expectKeywordFound :
                        continue

                    #exceptKeywordFound = False
                    #for j in range(len(exceptKeyword)):
                    #    if exceptKeyword[j] in description:
                    #        exceptKeywordFound = True
                    #        break
                    #
                    #if exceptKeywordFound:
                    #    continue

                    if ( previousPost == description[:10]) :
                        continue

                    tmpList = [i, regionList[i], description, dateFound, source]
                    resultSearchAll.append(tmpList)

                    previousPost = description[:10]

        else:
            print("Error Code:" + rescode)


#insta_searching(5)

for i in range(len(resultSearchAll)):
    print(resultSearchAll[i])

# 1 : blog, 0 : cafe
naver_searching(0)

naver_searching(1)

resultSearchAll.sort(key=lambda x: x[0])
for i in range(0, len(resultSearchAll)):
    print(resultSearchAll[i])
