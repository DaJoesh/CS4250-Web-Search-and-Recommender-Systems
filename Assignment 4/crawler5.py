from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

def parse_faculty_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    professors = []
    
    professor_divs = soup.find_all('div', class_='clearfix')
    
    for professor_div in professor_divs:

        professor = {}

        name_tag = professor_div.find('h2')
        if name_tag:
            professor['name'] = name_tag.text.strip()

        p_tag = professor_div.find('p')
        if p_tag:
            details = p_tag.find_all('strong')
            for detail in details:
                label = detail.text.strip().rstrip(':')
                value_tag = detail.find_next_sibling()
                if value_tag:
                    value = value_tag.text.strip()
                    professor[label.lower()] = value
        
        email_tag = p_tag.find('a', href=re.compile(r'^mailto:')) if p_tag else None
        if email_tag:
            professor['email'] = email_tag['href'][7:]
        
        website_tag = p_tag.find('a', href=re.compile(r'^https?://')) if p_tag else None
        if website_tag:
            professor['website'] = website_tag['href']
        
        if p_tag:
            p_text = p_tag.get_text()
            title_match = re.search(r'Title:\s*(.*?)\s*(Office:|$)', p_text)
            if title_match:
                professor['title'] = title_match.group(1).strip()
            office_match = re.search(r'Office:\s*(.*?)\s*(Phone:|$)', p_text)
            if office_match:
                professor['office'] = office_match.group(1).strip()
            phone_match = re.search(r'Phone:\s*(.*?)\s*(Email:|$)', p_text)
            if phone_match:
                professor['phone'] = phone_match.group(1).strip()
        
        professor.pop('web', None)
        
        if len(professor) > 1:
            professors.append(professor)
    
    return professors


def persist_professors_info(collection, professors):
    for professor in professors:
        collection.insert_one(professor)

def main():
    client = MongoClient()
    db = client['crawler_db']
    collection = db['pages']

    target_page = collection.find_one({'url': 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'})

    if target_page:
        professors_info = parse_faculty_info(target_page['html'])

        professors_collection = db['professors']

        persist_professors_info(professors_collection, professors_info)
        print("Faculty information parsed and persisted successfully.")
    else:
        print("Permanent Faculty page not found in the database.")

if __name__ == "__main__":
    main()