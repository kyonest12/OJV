import json

import requests
from bs4 import BeautifulSoup


api_url = 'https://www.topcv.vn/tim-viec-lam-moi-nhat'
domain = "https://www.topcv.vn/"
crsf_token = "MV2w9PPndSePL4xyFizWZHvF0fhhdDrX1r8hvpCj"

headers = {"X-Csrf-Token": crsf_token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61",
           "Cookie": "XSRF-iI6ImlYU1dLbXFWd2ZpbnZYMFhsUnFOQXc9PSIsInZhbHVlIjoiZkNaRVZXRlcxR2Vta1N0SExjM0lReTBSUWZ2cGl2UnNsNFlFK1EzRlNzSWZWWjd3cGdDK2MzcXNDeXowK3lQbU16aDJHTkJNamdJMUxSdndWK2tzcVRKMDJvTDJQdUgyM1lmZi9tVnJjMS9teUNUK0NCQUVNSVFYd2xlY2lzTFYiLCJtYWMiOiJkOTg3OWNjNzI2YzNlZjRjYmZlNjhmMzBiZDk1MTZkYWMyNzBiMmYzNjE1OGMwMmFjYjgyYmFiZmNhZTNhMjUzIiwidGFnIjoiIn0%3D; appier=%7B%22event%22%3A%22job_searched%22%2C%22payload%22%3A%7B%22searched_keyword%22%3A%22%22%2C%22job_category%22%3A%22%22%2C%22company_category%22%3A%22S%5Cu1ea3n%20xu%5Cu1ea5t%22%2C%22work_location%22%3A%22%22%7D%7D; topcv_session=eyJpdiI6IlhGMFRFOGlJbTZpNWRueHBIRkEvNFE9PSIsInZhbHVlIjoiemxxSGQ2MUV3QkJ1ZHFpRHFwMDFVazMvK0JrWkFhUlJPTkxmRXNHa2FPT1J3TDU2SzhFeVNpU09WODIvWFJwNjIvVkwybDNjT2RnSzJKdXdiaklHRkM3TndFeFRFdStBeDdiVEw3cDR2L0ZubnRKcmhLNWtpd0ZsbVR6dTNxMjAiLCJtYWMiOiI4ZDNkYTM3OTQ0NTQ2NjNjYzczNGRhNDlhZTNjMjY0ZjI2YzIxMDc0NmJiMzYyOTE3MTAyMzA3MDVjMmIzNDgwIiwidGFnIjoiIn0%3D"}

max_retries = 4
def retryResponse(url, params, post):
    response = None
    retries = 1
    while retries < max_retries:
        try:
            if post:
                response = requests.post(url, params=params, headers=headers)
            else:
                response = requests.get(url, params=params)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            if "Max retries exceeded" in str(e):
                pass
    return response

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
def crawData(idJob, detailUrl, dataConfig, pos):
    #detailUrl = "https://www.topcv.vn/brand/vuihoc/tuyen-dung/nhan-vien-kinh-doanh-sale-tu-van-khoa-hoc-tuyen-sinh-tai-trung-tam-thu-nhap-tu-12-30m-j1110734.html?ta_source=JobSearchList_LinkDetail&u_sr_id=vhUSrv4JrbT2iYcQuspU5ltBodv5GhVoiFX4BYwJ_1698225373"
    try:
        response = retryResponse(detailUrl, params={}, post=0)
        if response is None:
            print("failed")
            return None
        response = BeautifulSoup(response.text, 'html.parser')
        job = {}
        job["job_web"] = "https://www.topcv.vn/"
        job["job_id"] = idJob
        job["job_title"] = response.find("title").text.strip()

        if pos == 2:
            salaryIn = response.select_one(".box-main").select_one(".box-item").find("span").text.strip()
            job["job_salary"] = salaryIn

            job["job_place"] = ""
            typ = response.select_one(".box-address")

            value = typ.find_all('div', style="margin-bottom: 10px")
            for j in range(len(value)):
                job["job_place"] += value[j].text.strip() + ", "

        else:
            salaryIn = response.select(dataConfig["salaryIn"])
            for i in range(len(salaryIn)):
                typ = salaryIn[i].select_one(dataConfig["salary_type"]).text
                if typ == "Mức lương":
                    job["job_salary"] = salaryIn[i].select_one(dataConfig["salary_value"]).text
                    break

        detail = response.select(dataConfig["detail"])
        if len(detail) == 0:
            return None
        for i in range(len(detail)):
            typ = detail[i].find(dataConfig["detail_type"]).text
            value = detail[i].select_one(dataConfig["value"])
            if value is None:
                continue
            else:
                value = value.text.strip()
            if typ == "Mô tả công việc":
                job["job_description"] = value
            if typ == "Yêu cầu ứng viên":
                job["job_requirement"] = value
            if typ == dataConfig["benefit"]:
                job["job_benefit"] = value
            if typ == "Địa điểm làm việc":
                job["job_place"] = value
        return job
    except Exception as e:
        job = None
        return job

def getDetailJob(data):
    htmlPage = BeautifulSoup(data, 'html.parser')
    outputpath = "output.txt"
    with open(outputpath, "w", encoding="utf-8") as output_file:
        output_file.write(data)
    listJobHref = htmlPage.select(".job-item-default")
    for i in range(len(listJobHref)):
        a = listJobHref[i].find("a")
        idJob = listJobHref[i]["data-job-id"]
        detailUrl = a.get("href")
        print(detailUrl)
        job = None
        for j in range(len(config)):
            job = crawData(idJob, detailUrl, config[j], j)
            if job is not None:
                print(job)
                print("finish")
                print("_________________________________")
                break
        if job is None:
            print("failed")
            print("_____________________________")

params = {"page" : 1}
data = retryResponse(api_url, params=params, post=1).json()
max_page = data["data"]["total_page"]
while params["page"] <= max_page:
    data = retryResponse(api_url, params=params, post=1).json()
    htmlJob = data["data"]["html_job"]
    getDetailJob(htmlJob)
    params["page"] += 1


