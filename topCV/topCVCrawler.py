import json
import requests
import time
from bs4 import BeautifulSoup

api_url = 'https://www.topcv.vn/tim-viec-lam-moi-nhat'
domain = "https://www.topcv.vn/"
User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61"
res = requests.get(api_url)
ss = BeautifulSoup(res.text, 'lxml')
csrf_token = ss.select_one('meta[name="csrf-token"]')['content']
cookies = "XSRF-TOKEN="+res.cookies["XSRF-TOKEN"] + "; appier=" + res.cookies["appier"] + "; topcv_session=" + res.cookies["topcv_session"]

headers = {"User-Agent": User_Agent, "Cookie": cookies, "X-Csrf-Token": csrf_token}
max_retries = 4
def retryResponse(url, params, post):
    response = None
    time.sleep(5)
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
                print(e)
        retries += 1
        time.sleep(5)
    return response

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
def crawData(idJob, response, dataConfig, pos):
    #detailUrl = "https://www.topcv.vn/viec-lam/ke-toan-tong-hop/1145599.html?ta_source=JobSearchList_LinkDetail&u_sr_id=tRKKn4C2c9n83Ml4qhPOOJaGmM2UYbfb62cs8sHU_1698379975"
    try:
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
        print(e)
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
        job = None
        for j in range(len(config)):
            response = retryResponse(detailUrl, params={}, post=0)
            print(detailUrl)
            if response is None:
                print("failed")
                break
            response = BeautifulSoup(response.text, 'html.parser')
            job = crawData(idJob, response, config[j], j)
            if job is not None:
                print(job)
                print("finish")
                print("_________________________________")
                break
        if job is None:
            print("failed")
            print("_____________________________")


params = {"page" : 1}
dataRes = retryResponse(api_url, params=params, post=1)
print(api_url)
print(dataRes)
data = dataRes.json()
max_page = data["data"]["total_page"]
while params["page"] <= max_page:
    try:
        data = retryResponse(api_url, params=params, post=1).json()
        htmlJob = data["data"]["html_job"]
        getDetailJob(htmlJob)
        params["page"] += 1
    except Exception as e:
        print(e)
