from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import time

print('Looking for jobs in: ')
city = input('>')


def find_jobs():
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://www.linkedin.com/jobs/search?keywords=Software%2BEngineer&location=California%2C%20United%20States&locationId=&geoId=102095887&f_TPR=r86400&position=1&pageNum=0')
    previous_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        previous_height = new_height

    source_data = driver.page_source
    soup = BeautifulSoup(source_data, 'lxml')
    jobs = soup.find_all('div', class_='base-card base-card--link base-search-card base-search-card--link job-search-card')
    today = date.today().strftime("%b-%d-%Y")

    for job in jobs:
        location = job.find('span', class_='job-search-card__location').text.strip()
        if city in location:
            company_name = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_position = job.find('h3', class_='base-search-card__title').text.strip()
            more_info = job.a['href']
            with open(f'Job Listings/{today}.txt', 'a+') as f:
                f.write(f'Company Name: {company_name} \n')
                f.write(f'Job Position: {job_position} \n')
                f.write(f'Location: {location} \n')
                f.write(f'More Info: {more_info} \n\n')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 24
        time.sleep(time_wait * 3600)