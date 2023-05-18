import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objects as go
import streamlit as st
import matplotlib.font_manager  as fornm
from PIL import Image
import os
mpl.rcParams['font.family']  = 'Malgun Gothic'
import json
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.sidebar.title("서울시 공공자전거 활성화 방안 분석")
st.sidebar.header("22년도 이용현황 그래프")
list1 = ['월별이용현황','자치구별이용현황','시간대별이용현황']
select1 = st.sidebar.selectbox('Pick one',  list1)

def montly():
  st.snow()
  #데이터전처리 파일 불러오기
  df_12_daeyeo = pd.read_csv("3조_월별이용현황.csv", index_col=0) 


  # 이용 현황 데이터 표시
  st.subheader("['월별이용현황']")
  st.sidebar.width = 200
  st.dataframe(df_12_daeyeo, width=500) 

  st.write("")
  st.write("")

  # 월별이용현황 그래프 그리기
  fig = plt.figure()
  ax = plt.axes()
  plt.title('서울 공공자전거 월별 이용현황')
  plt.plot(df_12_daeyeo.index.astype(str),df_12_daeyeo.이용건수,label='이용건수(단위:백만명)',color = 'lightpink')
  plt.xticks(np.arange(0,13), rotation=45)
  plt.ylim(1300000,5000000)
  plt.legend(loc=(0,0))
  plt.xlabel('대여일자')
  plt.ylabel('이용건수')

  st.pyplot(fig, use_container_width=True)

if select1 == '월별이용현황':
  montly()

elif select1 == '자치구별이용현황':
  #데이터전처리 파일 불러오기
  df_last2 = pd.read_csv("3조_자치구별이용현황.csv", index_col=0) 


  #자치구별 이용현황 데이터 표시
  st.subheader(f"[{select1}]")
  st.sidebar.width = 200
  st.dataframe(df_last2, width=500) 

  st.write("")
  st.write("")

  #자치구별 이용현황 그래프 그리기
  fig = plt.figure(figsize=(40, 30)) # 도화지를 관리하는 변수
  ax = plt.axes() # 축을 관리하는 변수

  plt.bar(df_last2['소재지(위치)'], df_last2['이용건수'] ,color = 'gray')
  plt.xlabel('소재지(위치)', fontsize=50)
  plt.ylabel('이용건수', fontsize=50)
  plt.ylim(0, 4000000)
  plt.title('서울시내 구별 공공자전거 이용건수', fontsize=100)
  plt.xticks(fontsize=30,rotation=45)

  st.pyplot(fig, use_container_width=True)

elif select1 == '시간대별이용현황':
  #데이터전처리 파일 불러오기
  df_time_ = pd.read_csv("3조_시간대별이용현황.csv", index_col=0) 


  #시간대별 이용현황 데이터 표시
  st.subheader(f"[{select1}]")
  st.sidebar.width = 200
  st.dataframe(df_time_, width=500)
  fig = plt.figure(figsize=(40, 30))
  plt.title('시간대별 공공자전거 이용건수', fontsize=100)
  plt.bar(df_time_.index, df_time_['이용시간'], color=['lightblue', 'lightgreen'], alpha=0.5,label='22년12월기준')
  plt.xlabel('대여 시간',fontsize=50)
  plt.ylabel('이용시간(단위:만)',fontsize=50)
  plt.xticks(df_time_.index,fontsize=30)

  plt.twinx()
  plt.scatter(df_time_.index, df_time_['이동거리'], alpha=0.5)
  plt.ylabel('이동 거리(백만km)')

  st.pyplot(fig, use_container_width=True)


st.sidebar.header("이용 활성화 방안")
list2 = ['목표치설정','지도같이보기','활성화 방안 및 소감']
select2 = st.sidebar.selectbox('Pick one',  list2)


if select2 == '목표치설정':
  st.subheader(f"[{select2}]")
  st.text('''
            서울시 공공자전거 적자가 심각해 가격을 인상할 예정이라고 합니다
            평균 정기권:일일권 = 9:1 (12월비율)
            연간 10억을 메꾸려면
            정기권 대표- 30일권 1시간 (5000원) 18만건 
            일일권 대표- 일일권 1시간 (1000원) 10만건 
            더 채워야 합니다
    ''')
  st.write("현재 정기권 이용현황과 적자 10억을 줄이기 위한 정기권판매목표치 그래프")
  data = {'현재정기권추정치': [1277879, 1214416, 2181389, 3591456, 4466553, 3831023, 3691010, 3258524, 4284474, 4023229, 3454694, 1581029],
        '정기권목표치': [1457879, 1394416, 2361389, 3771456, 4646553, 4011023, 3871010, 3438524, 4464474, 4203229, 3634694, 1761029],
        }

  df119 = pd.DataFrame(data)
  df119.index = pd.RangeIndex(start=1, stop=len(df119)+1)

  st.dataframe(df119, width=500)

  fig = plt.figure()
  ax = plt.axes()
  plt.title('정기권 이용현황과 목표치')
  plt.plot(df119.index,df119.현재정기권추정치, label = '현재 정기권 이용건수(단위:백만명)',color = 'lightpink')
  plt.plot(df119.index,df119.정기권목표치, label = '정기권 이용 목표치',color = 'lightblue')
  plt.xticks(np.arange(1,13), rotation=45)
  plt.ylim(1300000,5000000)
  plt.legend(loc=(0))
  plt.xlabel('대여일자(월)')
  plt.ylabel('이용건수')

  st.pyplot(fig, use_container_width=True)

  st.write("현재 일일권 이용현황과 적자 10억을 줄이기 위한 일일권판매목표치 그래프")

  data1 = {'현재일일권예상치': [141986, 134935, 242376, 399050, 496283, 425669, 410112, 362058, 476052, 447025, 383854, 175669],
        '일일권목표치': [241986, 234935, 342376, 499050, 596283, 525669, 510112, 462058, 576052, 547025, 483854, 275669],
        }

  df120 = pd.DataFrame(data1)
  df120.index = pd.RangeIndex(start=1, stop=len(df120)+1)
  df120

  fig = plt.figure()
  ax = plt.axes()

  plt.title('일일권 이용현황과 목표치')
  plt.plot(df120.index,df120.현재일일권예상치,label = '현재 일일권 이용건수(단위:십만명)',color = 'lightpink')
  plt.plot(df120.index,df120.일일권목표치, label = '일일권 이용 목표치',color = 'lightblue')
  plt.xticks(np.arange(1,13), rotation=45)
  plt.ylim(130000,600000)
  plt.legend(loc=(0,0))
  plt.xlabel('대여일자(월)')
  plt.ylabel('이용건수')

  st.pyplot(fig, use_container_width=True)

elif select2 == '지도같이보기':
  #데이터전처리 파일 불러오기
  
  df_map_3 = pd.read_csv("3조_지도맵.csv", index_col=0) 
  df_map = pd.read_csv("3조_지도맵 df.csv", index_col=0) 
  geojson = json.load( open('seoulsigungu.geojson',encoding='utf-8')  )
  lat = df_map['위도'].mean()
  lng = df_map['경도'].mean()
  map = folium.Map( location = [ lat, lng ], zoom_start=11, tiles="CartoDB dark_matter" )

  folium.Choropleth(
  geo_data = geojson,
  data = df_map_3 ,
  columns = [df_map_3 .index, '이용건수'],
  fill_color='YlOrRd',
  key_on = 'properties.SIG_KOR_NM'
   ).add_to(map)
  # st.write(map)
  st_data = st_folium(map, width=725)
  
elif select2 == '활성화 방안 및 소감':
  st.subheader("분석 과정")
  st.write("""
  주제: 서울시 공공자전거 이용 활성화 방안

할일:
1. 현재 적자로 가격 요금 인상 불가피함 - 가격 요금 인상을 하지 않고도 얼만큼 이용을 해야 가격 요금인상 없이 지금처럼 이용할수 있을지? -> 필요 데이터 예시: 서울시 인구 대비 공공자전거 이용률 등등

2. 추천 구간 대신 이용량 늘리기 대체 방안 - 서울시 자치구 중에 따릉이 이용량, 이용시간대 등 가장 많고 적은 대비를 보여주는 구들을 찾아서 인사이트 분석하고 이용량 늘리는  활성화 방안 찾기
""")

  st.subheader("이용현황 분석 및 활성화 방안")
  st.write("""
  1. 3월-5월이 많고 9월에서 11월이 많다 / 12월-2월은 적다
     강서구, 송파구, 영등포구 순으로 많다 / 도봉구, 금천구, 강북구 적다
     오전 8시-9시, 오후 6시-7시가 많고 /  새벽시간대 적다
  2. 가격 인상을 막기 위한 목표치 설정 완료
  3. 영등포구 여의도 공원 한정해서라도 겨울에 공공자전거 옆에 자전거 장갑을 대여하도록 한다
     상대적으로 이용률이 적은 도봉,금천,강북은 대체로 산길이 많고 도로가 험하다는 인식이 있으므로 
      3개구 한정해서 자전거 도로 설치를 늘린다
     마라톤대회처럼 여름 새벽에 공공자전거 한강 라이딩 대회를 열어서 새벽시간대 이용률을 높인다""")

  st.subheader("소감")
  st.write("""
           명재/어려웠던 부분 : 원본데이터의 1월부터 6월까지의 대여일자는 str으로 되어있었고, 
           7월부터 12월까지는 int으로 되어있어서 그래프 x축으로 불러오는데 어려움이 있었으나,
           강사님의 도움으로 전체를 str으로 만들어 해결하였다!

        소감: 처음 시작했을땐 막막하고 해낼수 있을까 싶었는데, 
           좋은 팀원들과 강사님의 도움을 받아 끝까지 완성해서 너무 감사하고 뿌듯합니다 
           앞으로 더 열심히해서 다음번에는 더 잘할수있도록 노력하겠습니다!

        수현/어려웠던 점 : 목표치를 계산하기 위해서 산출해야 하는 값을 추정하고 계산하기 어려움
           소감: 배운 내용을 직접 적용해보니 더 기억에 잘 남았고 팀원들과 협동해서 과제를 해결하니 뿌듯했다


        병근/어려웠던 부분 : 데이터 자료가 내가 다루기에 불완전한 부분이 많았기 때문에 
           전처리과정에 있어서 어려움을 겪음 그래프도 조금더 명확고 다양하게 시각화시키고 싶었지만 
           나 자신의 역량부족으로 인해 기본값정도 밖에 구현해내지 못했다
        소감 : 매일매일 느끼는거지만 내가 아직 너무 부족하다는것을 더욱 느꼈고 
           당연한 얘기지만 더 열심히 해야겠다는 동기부여를 받았다. 

        지우/어려웠던 점: 공공데이터가 월별로 다 다른 방식으로 작성되어 있어서 탐색하는데 오래 걸렸다
        소감: 좋은 팀원들이 의견도 많이 내주고 다같이 협동해서 완성된 결과를 만들어낸 것 같아서
           보람찬 프로젝트였다! 모두들 고생했어요~
           """)

