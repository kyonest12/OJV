import requests
from bs4 import BeautifulSoup
import json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
headers = {"User-Agent": user_agent}
slug = {}
params = {"page": 0}


def writeToJson(jsonData):
    output_file_path = "output.json"

    with open(output_file_path, "w") as output_file:
        # Sử dụng json.dump để ghi dữ liệu vào tệp
        json.dump(jsonData, output_file, indent=4, separators=(',', ': '))


def crawData(detailJobUrl):

    #detailJobUrl = "https://vieclam24h.vn/marketing/seo-manager-c12p122id200268806.html"
    job = {}
    job["job_web"] = domain

    detailData = getJsonData(detailJobUrl, params={})
    data = detailData["props"]["initialState"]["api"]["jobDetailHiddenContact"]["data"]
    writeToJson(data)
    job["jobId"] = data["id"]
    job["job_title"] = data["title"]
    job["job_PostingDate"] = data["created_at"]
    job["job_requirement"] = data["job_requirement"]
    job["other_requirement"] = BeautifulSoup(data["other_requirement"], 'html.parser').text
    job["resume_requirement"] = BeautifulSoup(data["resume_requirement"], 'html.parser').text
    job["benefit"] = BeautifulSoup(data["benefit"], 'html.parser').text
    job["description"] = BeautifulSoup(data["description"], 'html.parser').text
    job["job_salary"] = f"{str(data['salary_min'])} - {str(data['salary_max'])}"
    job["job_location"] = ""
    job["job_field"] = ""

    occupations = data["occupation_ids_main"]
    for i in range(len(occupations)):
        job["job_field"] += slug[occupations[i]] + ", "
    places = data["places"]
    for i in range(len(places)):
        if places[i]["address"] is not None:
            job["job_location"] += places[i]["address"] + ", "
    print(job)

    print("finish")
    print("_________________________________________________")


def getDetailJob(jsonData):
    data = jsonData["props"]["initialState"]["api"]["searchJob"]["data"]

    items = data["items"]
    for i in range(len(items)):
        occupationId = items[i]["occupation_ids_main"][0]
        provincesId = items[i]["province_ids"][0]
        jobId = items[i]["id"]
        detailJobURL = domain + slug[items[i]["occupation_ids_main"][0]] + '/' + items[i][
            "title_slug"] + f'-c{occupationId}p{provincesId}id{jobId}.html'

        crawData(detailJobURL)
    # print(detailJobURL)


def getJsonData(URL, params):
    print(URL)
    if "page" in params:
        print(f"page : {params['page']}")
    response = requests.get(URL, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select_one('script[id="__NEXT_DATA__"]').text
    json_data = json.loads(data)
    return json_data


url_main = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh"
domain = "https://vieclam24h.vn/"
jsonData = getJsonData(url_main, params={})
occupationValue = jsonData["props"]["initialState"]["api"]["initCommon"]["data"]["occupation"]
for i in range(len(occupationValue)):
    slug[occupationValue[i]["id"]] = occupationValue[i]["slug"]

total_pages = jsonData["props"]["initialState"]["api"]["searchJob"]["data"]["total_pages"]

for i in range(1, total_pages + 1):
    params["page"] = i
    jsonData = getJsonData(url_main, params)
    getDetailJob(jsonData)

'''output_file = "out.json"
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)'''
