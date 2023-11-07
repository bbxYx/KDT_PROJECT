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


#---------------------------------------------------------------------------------------------------------------------------
# 위도 경도 구하기
tour_review.to_excel('tour_review.xlsx')
tour_info = pd.read_csv('tour_info.csv')
try : tour_info.drop('Unnamed: 0', axis = True, inplace=True)
except : pass

tour_info.to_excel('tour_info.xlsx')

df_addr = pd.read_excel('tour_addr.xlsx')
try : df_addr.drop('Unnamed: 0', axis = True, inplace=True)
except : pass

# 위도 경도 구하는 함수 사용
# lat = 위도, lng = 경도

def lat(address):
    from geopy.geocoders import Nominatim
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    lat = geo.latitude
    return lat

def lng(address):
    from geopy.geocoders import Nominatim
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    lng = geo.longitude
    return lng

def geocoding(address):
    from geopy.geocoders import Nominatim
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": geo.latitude, "lng": geo.longitude}
    return crd

addr_list_2 = df_addr.주소_2.to_list()

lat_list = []
lng_list = []

for i in tqdm(addr_list_2):
    try : 
        lat_ = lat(i)
        lng_ = lng(i)
    except : lat_,lng_ = 0,0
    
    lat_list.append(lat_)
    lng_list.append(lng_)

df_addr['위도']=lat_list
df_addr['경도']=lng_list

df_addr.to_excel('tour_addr_final.xlsx')
df_addr.dropna(axis=1, inplace=True)
df_addr.isna().sum()

df_tour = pd.read_excel('daegu.xlsx')
try : df_tour.drop('Unnamed: 0', axis = True, inplace=True)
except : pass
df_tour

tour_add_list = df_tour.주소_02.to_list()

lat_list = []
lng_list = []

for i in tqdm(tour_add_list):
    try : 
        lat_ = lat(i)
        lng_ = lng(i)
    except : lat_,lng_ = 0,0
    
    lat_list.append(lat_)
    lng_list.append(lng_)

df_tour['위도']=lat_list
df_tour['경도']=lng_list

df_tour.to_excel('daegu_final.xlsx')

# place1 = (lat1, lng1)
# place2 = (lat2, lng2)

def return_distance(place1, place2):
    import geopy.distance
    distance=geopy.distance.distance(place1, place2)

    return distance

# -------------------------------------------------------------------------------------------------
# 결과출력
# 파일불러오기
addr = pd.read_csv('tour_addr_1.csv')
info = pd.read_csv('tour_info_1.csv')
review = pd.read_csv('tour_review_1.csv')
food = pd.read_csv('daeguFood.csv')

def int_change(x) :
    try : x = int(x)
    except : x= np.nan
    return x

dis_list=[]

loc = '대구 남구 대명동 1501-2'
distance = 3

loc = return_latloc(loc)

for i in range(len(addr.index)):
    try : 
        dis = return_distance(loc, (addr.iloc[i]['lat'],addr.iloc[i]['lng']))
    except : dis = np.nan
    dis_list.append(dis)
addr['거리'] = dis_list

# 지정한 거리 안에 있는 곳 모두 뽑기
addr = addr[addr['거리']<distance]
addr_list = addr.name.unique()

# 지정한 거리안에 있는 곳 중 리뷰가 가장 많은 곳
review_cnt = []
for a in addr_list:
    review_ = review[review['name']==a]
    review['review_count'] = review.apply(lambda x : int_change(x['review_count']), axis=1)
    cnt_ = review_.review_count.sum()
    review_cnt.append([cnt_,a])

review_cnt

review_cnt.sort(reverse=True)

best = review_cnt[0]

a1 = review[review['name']==best[1]].review.to_list()
b1 = review[review['name']==best[1]].review_count.to_list()
review_result = []
for __ in range(len(a1)):
    review_result.append([a1[__],b1[__]])
review_result = " ".join(str(x) for x in review_result)

# 출력화면

print(f'''
당신에게 추천하는 최고의 놀거리 장소는 [{best[1]}]입니다.

현재 위치와의 거리는 {addr[addr['name']==best[1]].거리.to_list()[-1]}km입니다.

이 장소에 대한 정보입니다.
{info[info['name']==best[1]]['info'].to_list()[-1]}

이 장소에 대한 사람들의 평가입니다.
{review_result}''')

'''
당신에게 추천하는 최고의 놀거리 장소는 [이월드]입니다.

현재 위치와의 거리는 1.9063859947548971 kmkm입니다.

이 장소에 대한 정보입니다.
이월드는 1987년 10월 타워건립 및 종합테마파크 조성공사 재 착공을 시작으로 1993년 종합 테마파크 마스트플랜을 확정한 후 1995년 3월 개장한 폭포, 분수, 조명, 꽃으로 장식된 유럽식 도시공원으로 남녀노소 누구나 즐길 수 있는 놀이기구, 전시. 예술공간, 깔끔한 식당가 등이 마련되어 있다. 이월드에는 각 테마별로 광장을 만들어 방문객으로 하여금 새로움과 즐거움을 선사하고 있다. 매표소를 거쳐 들어서는 입구에 진입광장, 랜드의 중앙에 위치한 중앙광장, 어린이들의 놀이터 어린이광장, 젊은이들을 위한 공간이 영타운광장 등이 대표적인 광장이다.

이 장소에 대한 사람들의 평가입니다.
['놀이기구가 다양해요', 7211.0] ['볼거리가 많아요', 6267.0] ['아이와 가기 좋아요', 4464.0] ['사진이 잘 나와요', 4067.0] ['주차하기 편해요', 3543.0]
'''


# 최종 코드
# 입력 정보
loc= input('현재 위치의 주소를 입력하세요 : ')

kind = input('원하는 코스를 선택하세요(ex_밥,카페,영화/전시,놀거리) : ')

distance = int(input('검색을 원하는 반경(Km)를 입력하세요 : '))


# 처리/출력 정보
loc = return_latloc(loc)

if kind == '밥' : 
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim

    # 주소 => 위도 경도
    def address_to_coordinates(address):
        geolocator = Nominatim(user_agent="address-to-coordinates")
        location = geolocator.geocode(address)
        my_lat = location.latitude
        my_lon = location.longitude
        return my_lat, my_lon
    
    # 근처 음식점 반환
    def find_nearby_stores(my_lat, my_lon, radius_km, store_data):
        nearby_stores = []

        for _, row in store_data.iterrows():
            store_lat, store_lon = row['위도'], row['경도']
            distance = geodesic((my_lat, my_lon), (store_lat, store_lon)).kilometers

            if distance <= radius_km:
                store_info = {
                    '가게명': row['가게명'],
                    '주소': row['주소'],
                    '전화번호': row['전화번호']
                }
                nearby_stores.append(store_info)

        return nearby_stores

    store_data = pd.read_csv('daeguFood.csv')

    coordinates = address_to_coordinates(loc)
    my_latitude =coordinates[0]
    my_longitude = coordinates[1]

    nearby_stores = find_nearby_stores(my_latitude, my_longitude, distance, store_data)
    nearby_df = pd.DataFrame(nearby_stores)
    print(f'{distance}km이내의 맛집리스트')
    print(nearby_df)
                                                                

elif kind == '카페' : 
    cafe_df = pd.read_csv('cafe.csv')

    cafe_df['위도, 경도'] = list(zip(cafe_df['위도'], cafe_df['경도']))

    dit=[]

    place='대구 달서구 장기로 206'
    loc = return_latloc(place)

    for i in list(cafe_df['위도, 경도']):
        dit.append(return_distance(i, loc))

    cafe_df['거리']=dit

    min_dit=cafe_df.sort_values(by=['거리'])
    top5=min_dit.head(5)
    top5=top5.sort_values(by='방문자리뷰',ascending=False)

    print(f'현재 장소는... {place}')
    print('-'*20)
    print()
    print(f'현재 가장 가까운 카페는')
    print('- '*20)
    print()

    for n in range(5):
        print(f"가게이름 : {top5['가게이름'].iloc[n]}")
        print(f"리뷰갯수 : {top5['방문자리뷰'].iloc[n]}개")
        print(f"가게주소 : {top5['주소'].iloc[n]}")
        print(f"전화번호 : {top5['전화번호'].iloc[n]}")
        print(f"떨어진 거리 : {top5['거리'].iloc[n]}")
        print()
        print('- '*20)
        print()

elif kind == '영화' or kind == '전시' or kind == '영화/전시' :
        # mariadb에서 데이터 빼와서 데이터프레임으로 만들기

    # SQLAlchemy 엔진 생성
    engine = create_engine('mysql+pymysql://member3:member3@172.20.41.42:3307/ProjectDB')

    # SQL 쿼리 실행 및 결과를 데이터프레임으로 변환
    interpark_df = pd.read_sql('SELECT * FROM interpark', con=engine)
    cgv_df = pd.read_sql('SELECT * FROM cgv', con=engine)

    cgv_df = cgv_df.drop(columns='index')
    interpark_df = interpark_df.drop(columns='index')

    # 위도, 경도 시리즈를 묶어 하나의 시리즈로 합치기
    cgv_df['위도, 경도'] = list(zip(cgv_df['위도'], cgv_df['경도']))
    interpark_df['위도, 경도'] = list(zip(interpark_df['위도'], interpark_df['경도']))
    
    
    ans = input('영화 / 전시 선택하세요 : ')
    if ans=='영화':
        dit=[]

        for i in list(cgv_df['위도, 경도']):
            dit.append(return_distance(i, loc))

        cgv_df['거리'] = dit

        min_dit = cgv_df['거리'].min()
        df_selected = cgv_df[(cgv_df['거리'] == min_dit)]


        print("현재위치에서 가장 가까운 영화관 정보는 : ")
        print(df_selected['loc'].unique())
        print("입니다.")

        import time

        now = time
        now.localtime()

        today = int(str(now.localtime()[0]) + str(now.localtime()[1]) + str(now.localtime()[2]))

        today

        print("해당영화관의 현재 상영정보입니다.")
        df_selected_ = df_selected[(df_selected['date'] == today)]


        from tabulate import tabulate
        print(tabulate(df_selected_[['title', 'time']], headers='keys', tablefmt='fancy_outline'))
    

        # 나중에 또 입력될수 있으므로, 거리 정보 지운다.
        cgv_df = cgv_df.drop(columns='거리')
        cgv_df


    elif ans=='전시':
        dit=[]

        for i in list(interpark_df['위도, 경도']):
            dit.append(return_distance(i, p1))

        interpark_df['거리'] = dit

        min_dit = interpark_df['거리'].min()
        df_selected = interpark_df[(interpark_df['거리'] == min_dit)]


        print("현재위치에서 가장 가까운 전시 정보는 : ")
        print(df_selected['location'].unique())
        print("입니다.")

        print("해당전시장의 전시정보입니다.")

        from tabulate import tabulate
        print(tabulate(df_selected[['title', 'date']], headers='keys', tablefmt='fancy_outline'))

        # 나중에 또 입력될수 있으므로, 거리 정보 지운다.
        interpark_df = interpark_df.drop(columns='거리')
        interpark_df
    
    else:
        print("잘못된 입력!")


elif kind == '놀거리' : 

    addr = pd.read_csv('tour_addr_1.csv')
    info = pd.read_csv('tour_info_1.csv')
    review = pd.read_csv('tour_review_1.csv')

    dis_list=[]
    
    for i in range(len(addr.index)):
        try : 
            dis = return_distance(loc, (addr.iloc[i]['lat'],addr.iloc[i]['lng']))
        except : dis = np.nan
        dis_list.append(dis)
    addr['거리'] = dis_list

    # 지정한 거리 안에 있는 곳 모두 뽑기
    addr_ = addr[addr['거리']<distance]
    addr_list = addr_.name.unique()
    if len(addr_list) != 0 :

        # 지정한 거리안에 있는 곳 중 리뷰가 가장 많은 곳
        review_cnt = []
        for a in addr_list:
            review_ = review[review['name']==a]
            review['review_count'] = review.apply(lambda x : int_change(x['review_count']), axis=1)
            cnt_ = review_.review_count.sum()
            review_cnt.append([cnt_,a])
        
        review_cnt

        review_cnt.sort(reverse=True)

        best = review_cnt[0]

        a1 = review[review['name']==best[1]].review.to_list()
        b1 = review[review['name']==best[1]].review_count.to_list()
        review_result = []
        for __ in range(len(a1)):
            review_result.append([a1[__],b1[__]])
        review_result = " ".join(str(x) for x in review_result)

        # 출력화면
        print(f'''
        당신에게 추천하는 최고의 놀거리 장소는 [{best[1]}]입니다.

        현재 위치와의 거리는 {addr_[addr_['name']==best[1]].거리.to_list()[-1]}km입니다.

        이 장소에 대한 정보입니다.
        {info[info['name']==best[1]]['info'].to_list()[-1]}

        이 장소에 대한 사람들의 평가입니다.
        {review_result}''')
    else : print(f'반경 {distance}km내에는 적합한 장소가 없습니다.')
    
else : print('다시입력해주세요')