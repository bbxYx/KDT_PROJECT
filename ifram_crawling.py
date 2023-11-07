# 대구의 관광지를 검색해서 crawling을 하려고 합니다.
# iframe이 있어 까다로운 부분이 있습니다.
# 크롤링 한 정보를 DB에 담는 부분까지 구현한 코드입니다.

import pandas as pd
import mariadb as mdb
from tqdm import tqdm # for문의 진행상황 확인

# 크롤링
df_tour = pd.read_excel('daegu.xlsx')

tourList=df_tour.관광지.to_list()
len(tourList)

# 개수가 너무 적어 크롤링 결정

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# 관광지 행을 리스트로 만들기
df_tour.관광지.to_list()

# 개수가 적은 리스트로 크롤링이 잘 되는지 확인

driver = webdriver.Chrome()
driver.get("https://www.naver.com/")
driver.implicitly_wait(10) # 정보가 모두 뜰때까지 최대 10초를 기다린다.
time.sleep(3)

for i in tourList:
    search=driver.find_element(By.ID, "query")
    search.send_keys(i)
    time.sleep(1)
    search.send_keys(Keys.RETURN)

# 관광지의 이름을 알고있을때 크롤링
import time

import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 리뷰추출함수
def extract_review():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 리뷰 추출
    rev = []  # 추출한 리뷰 저장
    for i in range(1, 11): # 더보기 누르지 않은 상태로 최대 10개
        try:  # 사진 없는 후기는 div 3번째에 텍스트 위치
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[3]/div[4]/div[1]/ul/li['+str(i)+']/div[3]/a').send_keys(Keys.ENTER) # 텍스트 전체 볼 수 있게 클릭
            time.sleep(2)
            comment = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[3]/div[4]/div[1]/ul/li['+str(i)+']/div[3]/a/span').text  # 리뷰
            rev.append(comment)
        except: # 사진 있는 후기는 div 4번째에 텍스트가 위치
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[3]/div[4]/div[1]/ul/li['+str(i)+']/div[4]/a').send_keys(Keys.ENTER)
            time.sleep(2)
            comment = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[3]/div[4]/div[1]/ul/li['+str(i)+']/div[4]/a/span').text  # 리뷰
            rev.append(comment)
    return rev


# 리뷰 담는 리스트
data = []

# 크롬 드라이버 실행
driver = webdriver.Chrome()

for i in tqdm(tourList):
    # 검색창에 입력하지 않고 직접 해당 업소의 주소로 이동
    url = f'https://map.naver.com/p/search/{i}?c=15.00,0,0,0,dh'
    driver.get(url)
    time.sleep(8)

    
    try: 
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="entryIframe"]')) # iframe 이동
        time.sleep(3) 
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # 리뷰 탭으로 이동
        lists = soup.select('#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span')
        
        # 별점/방문자리뷰/블로그리뷰 순일때 방문자리뷰는 두번째에 위치=span[2]
        if len(lists) > 2: 
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[2]/a').send_keys(Keys.ENTER) # 방문자 리뷰
            time.sleep(3)
		
        # 방문자리뷰/블로그리뷰 순일때 방문자리뷰는 첫번째에 위치=span[1]
        else: 
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[1]/a').send_keys(Keys.ENTER) # 방문자 리뷰
            time.sleep(3)
        
        review = extract_review() # 리뷰 추출 함수 호출
        data.append(review)
        # print(review)
    
    except:
        data.append(' ')
        # print(' ')


# 대구 관광지를 검색해서 나오는 항목을 눌러서 동적크롤링하기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm_gui

driver = webdriver.Chrome()
driver.get("https://map.naver.com/v5/")
driver.implicitly_wait(10) # 정보가 모두 뜰때까지 최대 10초를 기다린다.
time.sleep(3)

# 키워드 변경가능
search = "대구 가볼만한곳"

# 검색창에 검색어 입력하기
search_box = driver.find_element(By.CSS_SELECTOR,"div.input_box>input.input_search")
search_box.send_keys(search)
time.sleep(2)

# 검색버튼 누르기
search_box.send_keys(Keys.ENTER)

name_list=[]
addr_list=[]
# frame = driver.find_element(By.TAG_NAME, 'iframe')

# 첫번째 프레임
frame=driver.find_element(By.CSS_SELECTOR,"iframe#searchIframe")
# print(frame)
# driver.switch_to.frame(frame)
driver.switch_to.frame(frame)

# 페이지 넘기기
pnum=1
pagenumlist={'1'}
while str(pnum) in pagenumlist:
    pagenumlist=[]
    plist=driver.find_elements(By.CLASS_NAME,"mBN2s ")
    for page in plist:
        pagenumlist.append(page.text)

    # 스크롤 끝까지 내리기
    scroll = driver.find_element(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]')
    driver.execute_script("arguments[0].scrollBy(0,2000)", scroll)
    time.sleep(2)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
    time.sleep(2)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
    time.sleep(2)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
    time.sleep(2)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
    time.sleep(2)
    driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
    time.sleep(2)

    # 페이지 넘기기
    rpage=driver.find_elements(By.CSS_SELECTOR,"a:nth-child(7) > svg")

    # 대구 놀거리 
    nav=driver.find_elements(By.CSS_SELECTOR,"div > span.place_bluelink.xBZDS")
    # print(nav)
    

    cnt=1
    for i in nav:
        if cnt==1:
            # 클릭
            i.click()
            time.sleep(2)
            driver.switch_to.default_content()
            #-----------------------------------------------------------------------
            # 두번째 프레임
            entframe=driver.find_element(By.CSS_SELECTOR,"iframe#entryIframe")
            print(entframe)
            driver.switch_to.frame(entframe)
            # 장소명, 주소 
            name=driver.find_element(By.CLASS_NAME,'Fc1rA').text
            addr=driver.find_element(By.CLASS_NAME,'LDgIH').text
            name_list.append(name)
            addr_list.append(addr)
            # 두번째 프레임 나오기
            driver.switch_to.default_content()
            #-----------------------------------------------------------------------
            cnt+=1

        else:
            driver.switch_to.frame(frame)
            # 클릭
            i.click()
            time.sleep(2)
            driver.switch_to.default_content()
            #-----------------------------------------------------------------------
            # 두번째 프레임
            entframe=driver.find_element(By.CSS_SELECTOR,"iframe#entryIframe")
            print(entframe)
            driver.switch_to.frame(entframe)
            # 장소명, 주소 
            name=driver.find_element(By.CLASS_NAME,'Fc1rA').text
            addr=driver.find_element(By.CLASS_NAME,'LDgIH').text
            name_list.append(name)
            addr_list.append(addr)

            # 두번째 프레임 나오기
            driver.switch_to.default_content()
            #-----------------------------------------------------------------------
            cnt+=1
        # 페이지 넘기기  
    driver.switch_to.frame(frame)  
    rpage[0].click()

    # rpage=driver.find_elements(By.CSS_SELECTOR,"a:nth-child(7) > svg")
    # rpage[0].click()
    time.sleep(2)
    pnum+=1

# 네이버지도가 아닌 홈 화면에서 크롤링하기
driver = webdriver.Chrome()
# star_list = []
review_list = []
review_count_list = []
info_list = []

for i in name_list:
    driver.get("https://www.naver.com/")
    driver.implicitly_wait(10) # 정보가 모두 뜰때까지 최대 10초를 기다린다.
    time.sleep(3)
    search=driver.find_element(By.ID, "query")
    search.send_keys(i)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    
    
    # 리뷰
    reviews = driver.find_elements(By.CLASS_NAME,'nWiXa')
    review = []
    for r in reviews:
        _ = r.text
        _ = _.replace('"','')
        review.append(_)
    review_list.append(review)   

    # 리뷰 개수
    review_counts = driver.find_elements(By.CLASS_NAME,'TwM9q')
    review_count = []
    for r in review_counts:
        _ = r.text
        try : _ = _.split('\n')[1]
        except : pass
        review_count.append(_)
    review_count_list.append(review_count) 

    # 소개
    a = "#place-main-section-root > section > div > div.place_section.no_margin.vKA6F.Aqsow > div > div > div.O8qbU.dRAr1 > div > a > span.rvCSr"
    try: 
        if driver.find_elements(By.CLASS_NAME,'zPfVt')[-1].text[-3:]=='...':
            info_link = driver.find_element(By.CSS_SELECTOR, a)
            info_link.click()
            info = driver.find_elements(By.CLASS_NAME,'zPfVt')[-1].text
        elif driver.find_elements(By.CLASS_NAME,'zPfVt')[-1].text[-3:]!='...' and driver.find_elements(By.CLASS_NAME,'zPfVt')[-1].text[-1]!='분':
            info = driver.find_elements(By.CLASS_NAME,'zPfVt')[-1].text
        else : info = 0
        info_list.append(info)
    except:
        info_list.append(0)

    # 별점 
    # star = driver.find_element(By.CLASS_NAME,'div.zD5Nm.kN1U_ > div.dAsGb > span.PXMot.LXIwF > em').text
    # # star = driver.find_element(By.CLASS_NAME,'place_blind').find_element(By.TAG_NAME,'em').text
    # print(star)
    # if len(star) != 0:
    #     star_list.append(star)
    # else : star_list.append(0)
    
    time.sleep(3)

tour_addr = pd.DataFrame({'관광지명':name_list, '주소':addr_list})
tour_review = pd.DataFrame({'관광지명':name_list, '리뷰':review_list, '리뷰개수':review_count_list})
tour_info = pd.DataFrame({'관광지명':name_list, '정보':info_list})

tour_addr.to_csv('tour_addr.csv')
tour_review.to_csv('tour_review.csv')
tour_info.to_csv('tour_info.csv')


#---------------------------------------------------------------------------------
# DB
import mariadb as mdb

conn_params = {'host':'172.20.41.42',
               'user':'member1',
               'passwd' : 'member1', 
               'port' : 3307,
               'db' : 'ProjectDB',
               'autocommit' : True}
import pandas as pd

addr = pd.read_excel('tour_addr_final.xlsx')
try : addr.drop('Unnamed: 0', inplace=True, axis=1)
except : pass
review = pd.read_excel('tour_review.xlsx')
try : review.rename(columns={'Unnamed: 0':'번호'}, inplace=True)
except : pass
info = pd.read_excel('tour_info.xlsx')
try : info.drop('Unnamed: 0', inplace=True, axis=1)
except : pass

try :
    # mariadb연결
    connDB = mdb.connect(**conn_params)

    # DB에 접근할 수 있는 cursor객체 가져오기
    cursor = connDB.cursor()

    # 데이터베이스 테이블 만들기
    cursor.execute("create table tour_addr(name varchar(20) not null primary key, address varchar(40) not null, lat float, lng float);")
    cursor.execute("create table tour_info(name varchar(20) not null primary key, info varchar(5000));")
    cursor.execute("create table tour_review(name varchar(20) not null, review varchar(1000),review_count int) AUTO_INCREMENT=1;")

    # tour_addr에 데이터 넣기
    for i in range(len(addr.index)):
        name_,addr_,lat_,lng_ = addr.iloc[i]['관광지명'], addr.iloc[i]['주소_1'], addr.iloc[i]['위도'], addr.iloc[i]['경도']
        # print(name_,addr_,lat_,lng_)
        cursor.execute("insert into tour_addr(name, address, lat, lng) values(?,?,?,?);",
                    [name_,addr_,lat_,lng_])

    # tour_info에 데이터 넣기
    for i in range(len(info.index)):
        name_,info_ = info.iloc[i]['관광지명'], info.iloc[i]['정보']
        # print(name_,info_)
        cursor.execute("insert into tour_info(name, info) values(?,?);",
                    [name_,info_])

    # tour_review에 데이터 넣기
    for i in range(len(review.index)):
        name_,review_,review_count_ = review.iloc[i]['관광지명'], review.iloc[i]['리뷰'], review.iloc[i]['리뷰개수']
        review_ = review_.split(',')
        review_count_ = review_count_.split(',')
        # print(name_,review_,len(review_),review_count_, len(review_count_) )
        for j in range(len(review_)):
            review_[j]=review_[j].replace('[','').strip()
            review_[j]=review_[j].replace(']','').strip()
            review_[j]=review_[j].replace("'",'').strip()
            review_count_[j]=review_count_[j].replace('[','').strip()
            review_count_[j]=review_count_[j].replace(']','').strip()
            review_count_[j]=review_count_[j].replace("'",'').strip()
            try : 
                review_count_[j]=int(review_count_[j])
            except : review_count_[j]=0
            cursor.execute("insert into tour_review(name, review, review_count) values(?,?,?);",
                        [name_,review_[j],review_count_[j]])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    # 테이블에 있는 0, ''값을 null값으로 바꾸기
    cursor.execute('UPDATE tour_addr SET lat = CASE WHEN lat = 0 THEN NULL ELSE lat END;')
    cursor.execute('UPDATE tour_addr SET lng = CASE WHEN lng = 0 THEN NULL ELSE lng END;')
    cursor.execute('UPDATE tour_info SET info = CASE WHEN info = "0" THEN NULL ELSE info END;')
    cursor.execute('UPDATE tour_review SET review = CASE WHEN review = "" THEN NULL ELSE review END;')
    cursor.execute('UPDATE tour_review SET review_count = CASE WHEN review_count = 0 THEN NULL ELSE review_count END;')

    # 정리한 테이블 데이터로 내보내기

except mdb.Error as e :
    print(f'ERROR : {e}')
