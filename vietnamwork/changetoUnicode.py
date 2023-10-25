import json

# Bước 1: Đọc dữ liệu từ tệp JSON
try:
    with open("output.json", 'r') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

with open('output_chuan.txt', 'w', encoding="UTF-8") as txt_file:
    txt_file.write("[\n")
# Bước 2: Chuyển đổi dữ liệu thành văn bản chuẩn (text)
    for job_data in existing_data:
        job_title = job_data.get('job_tittle', 'N/A')
        job_requirement = job_data.get('job_requirement', 'N/A')
        job_posting_date = job_data.get('job_postingDate', 'N/A')
        job_rank = job_data.get('job_rank', 'N/A')
        job_career = job_data.get('job_career', 'N/A')
        job_field = job_data.get('job_field', 'N/A')
        job_skills = job_data.get('job_skills', 'N/A')
        job_cv_language = job_data.get('job_CVLanguage', 'N/A')
        job_description = job_data.get('job_description', 'N/A')
        job_location = job_data.get('job_location', 'N/A')
        job_salary = job_data.get('job_salary', 'N/A')

        # Ghi thông tin vào tệp văn bản
        txt_file.write("{\n")
        txt_file.write(f" \"Job Title\": \"{job_title}\"\n")
        txt_file.write(f" \"Job Requirement\": \"{job_requirement}\"\n")
        txt_file.write(f"\"Job Posting Date\": \"{job_posting_date}\"\n")
        txt_file.write(f"\"Job Rank\": \"{job_rank}\"\n")
        txt_file.write(f"\"Job Career\": \"{job_career}\"\n")
        txt_file.write(f"\"Job Field\": \"{job_field}\"\n")
        txt_file.write(f"\"Job Skills\": \"{job_skills}\"\n")
        txt_file.write(f"\"Job CV Language\": \"{job_cv_language}\"\n")
        txt_file.write(f"\"Job Description\": \"{job_description}\"\n")
        txt_file.write(f"\"Job Location\": \"{job_location}\"\n")
        txt_file.write(f"\"Job Salary\": \"{job_salary}\"\n")
        txt_file.write("},\n")
        #with open("output_chuan.txt", 'w', encoding='utf-8') as file:
            #file.write(existing_data[i])
    txt_file.write("]")

