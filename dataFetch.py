import requests
import json

#api-endpoint
keywordURL = "http://tools.kinds.or.kr:8888/topn_keyword"
featureURL = "http://tools.kinds.or.kr:8888/feature"
newsListURL = "http://tools.kinds.or.kr:8888/search/news"

#access keyword & feature
def getFeature(title,content):
    featureParams = {
    "access_key": "dd42d5f3-66a5-4d6b-a36b-ecf1a221bd52",
    "argument": {
        "title": title,
        "sub_title": "",
        "content": content
    }}
    r = requests.post(url = featureURL, json=featureParams)
    feature = r.json()
    return feature

def takeSecond(elem):
    return float(elem[1])

#request for 24 hour news
recentNewsParams = {
    "access_key": "dd42d5f3-66a5-4d6b-a36b-ecf1a221bd52",
    "argument": {
        "published_at": {
            "from": "2022-08-10",
            "until": "2022-08-11"
        },
                "provider": [
            ""
        ],
        "category": [
            "정치>정치일반"
        ],
        "category_incident": [
            ""
        ],
        "byline": "",
        "provider_subject": [
            ""
        ],
        "subject_info": [
            ""
        ],
        "subject_info1": [
            ""
        ],
        "subject_info2": [
            ""
        ],
        "subject_info3": [
            ""
        ],
        "subject_info4": [
            ""
                ""
        ],
        "sort": [{ "date":"desc" }, { "_score":"desc" }],
        "hilight": 0,
        "return_from": 0,
        "return_size": 20,
        "fields": [
            "title",
            "category",
            "news_id",
            "tms_raw_stream",
            "content",
            "provider"
        ]
    }        
}


#accessing data
newsListRequest = requests.post(url = newsListURL, json=recentNewsParams)

#changing json back to dict
newsList = newsListRequest.json()

#creating the input list
input = []
numOfInput = 0
for i in newsList.get("return_object").get("documents"):
    input.append([])
    #언론사
    input[numOfInput].append(i.get("provider"))

    #연관어 정리
    input[numOfInput].append(i.get("tms_raw_stream"))

    #특성 추출
    input[numOfInput].append(getFeature(i.get("title"),i.get("content")).get("return_object").get("result").get("title"))
    input[numOfInput].append(getFeature(i.get("title"),i.get("content")).get("return_object").get("result").get("content"))
    input[numOfInput][2] = input[numOfInput][2] + " " + input[numOfInput][3]
    del input[numOfInput][3]
    
    #본문
    input[numOfInput].append(i.get("content"))

    #데이터 리스트화
    input[numOfInput][1] = input[numOfInput][1].split("\n")
    input[numOfInput][1][:] = [x for x in input[numOfInput][1] if x]
    input[numOfInput][2] = input[numOfInput][2].split(" ")
    
    #상위 20개 특성 추출
    for i in range(len(input[numOfInput][2])):
      input[numOfInput][2][i] = input[numOfInput][2][i].split("|")
    input[numOfInput][2].sort(key=takeSecond, reverse = True)
    inputFeatures = list()
    if (len(input[numOfInput][2]) >= 20):
      for i in range(20):
        inputFeatures.append(input[numOfInput][2][i][0])
    else:
      del input[numOfInput]
      continue
    input[numOfInput][2] = inputFeatures

    #상위 20개 키워드 추출
    del input[numOfInput][1][20:]

    #본문 제외 값들 통합
    input[numOfInput][0] = [input[numOfInput][0]]
    input[numOfInput][0] = input[numOfInput][0] + input[numOfInput][1] + input[numOfInput][2]
    del input[numOfInput][1]
    del input[numOfInput][1]

    #index
    numOfInput += 1

#index 초기화
numOfInput = 0

#41개 이하 데이터들 삭제
for i in input:
    if (len(i) != 2):
      del input[numOfInput]
    if (len(i[0]) < 41):
      del input[numOfInput]
    #index
    numOfInput += 1


print(input)

for i in input:
  print("=========기사 시작 =========\n" + i[1])

print(len(input))