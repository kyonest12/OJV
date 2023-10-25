import requests
from bs4 import BeautifulSoup

max_retries = 4
def soupResponse(url, params):
    response = None
    retries = 1
    while retries < max_retries:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            if "Max retries exceeded" in str(e):
                pass
        retries += 1
    if response is None:
        print("max retries with this URL")
        print("_____________________________")
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def getText(basicInfo):
    str = ""
    contents = basicInfo.contents
    for i in range(1, len(contents)):
        str += contents[i].text.strip() + ', '
    return str


def crawData(detailUrl):
    job = {}
    job["job_web"] = domain

    print(detailUrl)
    soup = soupResponse(domain+detailUrl, params={})

    basicInfo = soup.select_one(".com_info").find('h1', class_='com_post')
    job["job_id"] = basicInfo['data-id']
    job["job_title"] = basicInfo.text

    basicInfo = soup.find_all("p", class_="index hidden_mobi")
    for i in range(len(basicInfo)):
        info = getText(basicInfo[i])
        type = basicInfo[i].contents[0].strip()
        if type == "Ngành nghề:":
            job["job_field"] = info
        if type == "Lĩnh vực:":
            job["job_career"] = info
        if type == "Mức lương:":
            job["job_salary"] = info

    detailInfo = soup.select(".detail_if")
    for i in range(len(detailInfo)):
        typ = detailInfo[i].find("p").text
        if typ == "Chức vụ":
            job["job_rank"] = detailInfo[i].find("span").text
        if typ == "Địa chỉ chi tiết":
            job["job_place"] = detailInfo[i].find("span").text

    detailInfo = soup.select(".mt_20")
    for i in range(len(detailInfo)):
        inf = []
        for j in range(len(detailInfo[i].contents)):
            text = detailInfo[i].contents[j].text.replace('\n', '').strip()
            if text != "":
                inf.append(text)
        if len(inf) == 1:
            inf.append("")
        if inf[0] == "MÔ TẢ CÔNG VIỆC":
                job["job_description"] = inf[1]
        if inf[0] == "YÊU CẦU":
                job["job_requirement"] = inf[1]
        if inf[0] == "QUYỀN LỢI":
            job["job_benefit"] = inf[1]
            break

    print(job)
    print("finish")
    print("____________________________")


def getDetailJobs(cateJobUrl):
    print(cateJobUrl)
    params = {"page": 1}
    while 1:
        listDetailJobsA = soupResponse(cateJobUrl, params=params).select(".item_cate")
        if len(listDetailJobsA) == 0:
            break
        for i in range(len(listDetailJobsA)):
            detailUrl = listDetailJobsA[i].find("a").get("href")
            crawData(detailUrl)
        params["page"] += 1



urlMain = "https://timviec365.vn/danh-sach-nganh-nghe"
domain = "https://timviec365.vn"
listCateJobA = soupResponse(urlMain, params={}).find(id="m_list_nganhnghe").find_all("a")
for i in range(len(listCateJobA)):
    cateJobUrl = domain + listCateJobA[i].get("href")
    getDetailJobs(cateJobUrl)
