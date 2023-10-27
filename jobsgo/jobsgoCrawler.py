import requests
from bs4 import BeautifulSoup
from lxml import etree
import json

file_path = "config.json"
with open(file_path, "r") as file:
    config = json.load(file)


def getData(detailURL):
    #detailURL = "https://jobsgo.vn/viec-lam/nhan-vien-kinh-doanh-ban-ghtn-dong-bac-bo-16205477338.html"
    print(detailURL)
    detailJob = BeautifulSoup(requests.get(detailURL).text, "html.parser")

    job = {}

    input_element = detailJob.find('input',
                                   {'class': 'form-control', 'id': 'reportform-job_id', 'name': 'ReportForm[job_id]'})
    if input_element:
        job["job_id"] = input_element['value']

    job["job_tittle"] = detailJob.select_one(f".{config['class-title']}").text
    #print(job["job_tittle"])

    job["job_salary"] = detailJob.select_one(f".{config['class-salary']}").text
    #print(job["job_salary"])

    basic_info = detailJob.select(f".{config['class-basic_info']}")
    for i in range(len(basic_info)):
        vp = basic_info[i].select("p")
        if len(vp) < 2:
            continue
        type = vp[0].text
        value = vp[1].text
        if type == "Tính chất công việc":
            job["job_characteristic"] = value
        if type == "Vị trí/chức vụ":
            job["job_position"] = value
        if type == "Ngày đăng tuyển":
            job["job_postingDate"] = value
        if type == "Yêu cầu bằng cấp (tối thiểu)":
            job["job_degree"] = value
        if type == "Yêu cầu kinh nghiệm":
            job["job_exp"] = value
        if type == "Yêu cầu độ tuổi":
            job["job_age"] = value

    detail_info = detailJob.select(f".{config['class-detail'][0]}")
    for i in range(len(detail_info)):
        info = detail_info[i].select_one(f".{config['class-detail'][1]}")
        if info is None:
            continue
        if info.text == "Địa điểm làm việc":
            place = detail_info[i].select_one(f".{config['class-detail_place']}").select("p")
            for i in range(len(place)):
                if i == 0:
                    job["job_place"] = place[i].text[2:].rstrip()
                else:
                    job["job_place"] += '\n' + place[i].text[2:].rstrip()

            #print(job["job_place"])
        if info.text == "Ngành nghề":
            field = detail_info[i].select_one(f".{config['class-detail_field']}").select("a")
            for i in range(len(field)):
                if i == 0:
                    job["job_field"] = field[i].text.rstrip()
                else:
                    job["job_field"] += '\n' + field[i].text.rstrip()
            #print(job["job_field"])
        if info.text == "Mô tả công việc":
            des = detail_info[i].select_one(f".{config['class-des-benefits-require']}")
            job["job_description"] = des.text
        if info.text == "Yêu cầu công việc":
            des = detail_info[i].select_one(f".{config['class-des-benefits-require']}")
            job["job_requirement"] = des.text
        if info.text == "Quyền lợi được hưởng":
            des = detail_info[i].select_one(f".{config['class-des-benefits-require']}")
            job["job_benefits"] = des.text

    job["job_web"] = "https://jobsgo.vn/"

    print(job)


def getLinkToDetail(html):
    html = html.select(".brows-job-company-img")
    for i in range(len(html)):
        url = html[i].select_one("a").get('href')
        try:
            getData(url)
            print("finish")
            print("_____________________________________")
        except Exception as e:
            print(e)
            return


initial_url = "https://jobsgo.vn"
cur_page = "/viec-lam-trang-1.html?view=ajax"

while (1):
    print(cur_page)
    response = requests.get(initial_url + cur_page)
    soup = BeautifulSoup(response.text, 'lxml')
    list_job = soup.select_one(f".{config['class-list_job']}")  # config['class-list_job']
    if list_job is None:
        break
    getLinkToDetail(list_job)
    cur_page = soup.select_one(".next").find("span").get("data-href")



