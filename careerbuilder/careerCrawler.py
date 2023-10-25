import requests
from bs4 import BeautifulSoup
import json
import re

max_retries = 4  # Số lần thử lại tối đa
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46'}

file_path = "config.json"
with open(file_path, "r") as file:
    config = json.load(file)


def normStr(str):
    words = str.split()
    output_string = ' '.join(words)
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', output_string)


def crawDetail(detailPage):
    noSearch = detailPage.select_one(".no-search")

    # job is expired
    if noSearch is not None:
        return None

    job = {}

    job["job_title"] = normStr(detailPage.select_one(".title").text)

    locate = detailPage.select_one(".map").find("p")
    if locate is not None:
        job["job_location"] = normStr(locate.text)

    detail_box = detailPage.select(f".{config['class-detail-box']}")
    for i in range(len(detail_box)):
        types = detail_box[i].find_all("ul")
        for j in range(len(types)):
            list = types[j].find_all("li")
            for k in range(len(list)):
                type = list[k].find("strong").text
                #print(type)
                if type == " Ngày cập nhật":
                    job["job_postingDate"] = normStr(list[k].find("p").text)
                    # print(list[k].find("p").text)

                if type == " Ngành nghề":
                    job["job_field"] = ""
                    fields = list[k].find("p").find_all("a")
                    for l in range(len(fields)):
                        job["job_field"] += normStr(fields[l].text.lstrip().rstrip()) + ', '

                if type == " Hình thức":
                    job["job_career"] = normStr(list[k].find("p").text)

                if type == " Lương":
                    job["job_salary"] = normStr(list[k].find("p").text)

                if type == "Kinh nghiệm":
                    job["job_exp"] = normStr(list[k].find("p").text)

                if type == "Cấp bậc":
                    job["job_rank"] = normStr(list[k].find("p").text)

                if type == "Hết hạn nộp":
                    job["job_expired"] = normStr(list[k].find("p").text)
                # print("___________________________________________-")

    detail_row = detailPage.select(f".{config['class-detail_row']}")
    for i in range(len(detail_row)):
        title = detail_row[i].select_one(f".{config['class-detail_title']}")
        if title is None:
            continue
        title = title.text
        #print(title)
        if title == "Phúc lợi ":
            job["job_benefits"] = normStr(detail_row[i].find("ul").text)
            #print(job["job_benefits"])

        if title == "Mô tả Công việc":
            #print(detail_row[i].text)
            job["job_description"] = normStr(detail_row[i].text)

        if title == "Yêu Cầu Công Việc":
            job["job_requirement"] = normStr(detail_row[i].text)
            #print(job["job_requirement"])

        if title == "Thông tin khác":
            job["job_otherInfo"] = normStr(detail_row[i].text)

    job["job_web"] = "https://careerbuilder.vn/"
    print(job)
    print("finish")
    print("_________________________________________________________")


def crawData(soup):
    job_item_list = soup.find(id="jobs-side-list-content").select(f".{config['class-job_item']}")
    for i in range(len(job_item_list)):
        job_item = job_item_list[i].find("a", class_=f"{config['class-job_link']}").get("href")
        print(job_item)
        detailPage = None
        retry = 0
        while retry < max_retries:
            print(retry)
            try:
                detailPage = requests.get(job_item, headers=headers)
                detailPage.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if "Max retries exceeded" in str(e):
                    pass

            retry += 1
        if detailPage is not None:
            detailPage = BeautifulSoup(detailPage.text, 'lxml')
            crawDetail(detailPage)
        else:
            print("max retries with this URL")
            print("____________________________________________")
            return



api_url = 'https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-'

count = 0
response = None

while 1:
    getURL = api_url + 'trang-' + str(count) + '-vi.html'
    print(getURL)
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(getURL, headers=headers)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            if "Max retries exceeded" in str(e):
                pass
        retries += 1
    if response is None:
        print("max retries with this URL")
        print("_____________________________")
        continue
    soup = BeautifulSoup(response.text, 'lxml')
    no_search = soup.select_one(f".{config['class-no_search']}")
    if no_search is not None:
        break
    crawData(soup)
    count += 1