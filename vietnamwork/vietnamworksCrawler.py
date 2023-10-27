import requests
from bs4 import BeautifulSoup
import json

#data_job = []

def saving(page, i):
    file_name = "saving_point.txt"

    with open(file_name, 'w') as file:
        file.write(f"page: {page}\n")
        file.write(f"count: {i}\n")

def get_detail_data_job(detailURL, page, count, jobId):
    file_path = "config.json"
    with open(file_path, "r") as file:
        config = json.load(file)
    print(config["class-requirements"])
    print("page: ", page, "stt: ", count)
    print(detailURL)
    try:
        job_value = requests.get(detailURL)
        # with open("output.txt", "w", encoding='utf-8') as file:
        # file.write(job_value.text)
        soup = BeautifulSoup(job_value.text, 'lxml')

        job = {}

        job["jobId"] = jobId

        job_requirement = soup.select_one(f".{config['class-requirements']}").text.lstrip().rstrip()

        job["job_requirement"] = job_requirement

        job_tittle = soup.find(f"{config['tag-title']}")
        job["job_tittle"] = job_tittle.text.lstrip()

        information = soup.select_one(f"div.{config['class-information']}")
        summary_item = information.select(f".{config['class-summary_item']}")
        for i in range(len(summary_item)):
            summary_content = summary_item[i].select_one(f".{config['class-summary_content']}")
            if summary_content is None:
                continue
            value = summary_content.select_one(f".{config['class-value']}")
            if value.text == "Ngày Đăng Tuyển":
                job_postingDate = summary_content.select_one(f".{config['class-content']}").text.lstrip().rstrip()
                job["job_postingDate"] = job_postingDate
            if value.text == "Cấp Bậc":
                job_rank = summary_content.select_one(f".{config['class-content']}").text.lstrip().rstrip()
                job["job_rank"] = job_rank
            if value.text == "Ngành Nghề":
                job_career = summary_content.select_one(f".{config['class-content']}").text.lstrip().rstrip()
                job["job_career"] = job_career
            if value.text == "Lĩnh vực":
                job_field = summary_content.select_one(f".{config['class-content']}").text.lstrip().rstrip()
                job["job_field"] = job_field
            if value.text == "Kỹ Năng":
                job_skills = summary_content.select_one(f".{config['class-content']}").text.lstrip().rstrip()
                job["job_skills"] = job_skills
            if value.text == "Ngôn Ngữ Trình Bày Hồ Sơ":
                job_CVLanguage = summary_content.select_one(f".{config['class-content']}").text.lstrip().rstrip()
                job["job_CVLanguage"] = job_CVLanguage

        job_benefits = []
        list_job_benefits = soup.select_one(f".{config['class-list_job_benefits'][0]}").select(f".{config['class-list_job_benefits'][1]}")
        for i in range(len(list_job_benefits)):
            job_benefits.append(list_job_benefits[i].select_one(f".{config['class-job_benefits.append']}").text.replace("-", "")
                                .replace("\n", "").rstrip(" "))

        job_description = soup.select_one(f".{config['class-job_description']}").text.lstrip().rstrip()
        job["job_description"] = job_description
        job_location = soup.select_one(f".{config['class-job_location']}").text.rstrip()
        job["job_location"] = job_location
        job_salary = soup.select_one(f".{config['class-job_salary']}").text.rstrip().strip()
        job["job_salary"] = job_salary


        job["job_web"] = "https://www.vietnamworks.com/"

        #data_job.append(job)
        print(job)
        print("_________________________________________")

        '''try:
            with open("output.json", 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []
        existing_data.append(job)
        with open("output.json", 'w') as file:
            json.dump(existing_data, file, indent=4)
        saving(page, count)'''

    except Exception as e:
        print(e)


api_url = 'https://ms.vietnamworks.com/job-search/v1.0/search'

data = {
    'hitsPerPage': 200,
    'page': 1,
}

detail_urls = []
count = 1
while 1:
    response = requests.post(api_url, json=data)
    json_data = response.json()
    if "data" not in json_data:
        print("finish")
        break
    else:
        data_value = json_data.get("data")
        for i in range(len(data_value)):
            detail_urls = data_value[i].get("jobUrl")
            get_detail_data_job(detail_urls, data["page"], i, data_value[i].get("jobId"))
        data['page'] += 1
        #count += 1