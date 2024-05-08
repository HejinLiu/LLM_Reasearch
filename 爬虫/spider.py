import os
import pandas as pd
from bs4 import BeautifulSoup


def scrape_jobs_from_html(html_content):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    jobs = []
    job_cards = soup.find_all('li', class_='job-card-wrapper')
    for job_card in job_cards:
        job_details = {}
        # 提取标题
        job_details["标题"] = job_card.find('span', class_='job-name').text.strip()
        # 提取公司
        job_details["公司"] = job_card.find('h3', class_='company-name').text.strip()
        # 提取薪水
        job_details["薪水"] = job_card.find('span', class_='salary').text.strip()
        # 提取工作地点
        job_details["工作地点"] = job_card.find('span', class_='job-area').text.strip()
        # 提取经验要求和学历要求
        job_info = job_card.find('div', class_='job-info')
        job_details["经验要求"] = job_info.find_all('li')[0].text.strip()
        job_details["学历要求"] = job_info.find_all('li')[1].text.strip()
        # 提取公司标签
        company_tags = job_card.find('ul', class_='company-tag-list').find_all('li')
        for i, tag in enumerate(company_tags, 1):
            job_details[f"公司标签{i}"] = tag.text.strip()
        # 提取福利信息
        job_details["福利信息"] = job_card.find('div', class_='info-desc').text.strip()

        jobs.append(job_details)

    return jobs


def save_to_excel(jobs, filename):
    df = pd.DataFrame(jobs)
    df.to_excel(filename, index=False)


if __name__ == "__main__":
    all_jobs = []
    for i in range(1, 11):
        with open(f"htmls/{i}.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        jobs_on_page = scrape_jobs_from_html(html_content)
        all_jobs.extend(jobs_on_page)

    save_to_excel(all_jobs, "jobs_from_htmls.xlsx")
