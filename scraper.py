import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from ddgs import DDGS

def save_output(location,data):
    output_file = 'output.txt'
    with open(os.path.join(location,output_file),'a',encoding='utf-8') as f:
        f.write(data)

def beautify_html(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    important_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    content = ''
    for tag in important_tags:
        content += tag.get_text(strip=True) + '\n'
    
    return content.strip()

def relevant_sites(search_about):
    
    results_list = []

    with DDGS() as ddgs:
        results = list(ddgs.text(search_about, max_results=5))
    
        for result in results:
            results_list.append(result['href'])
    return results_list

def main():
    search_for = str(input('Want to search about : '))
    sites = relevant_sites(search_about=search_for)
    for site in sites:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        page = requests.get(site, headers=headers, timeout=10)
        page.encoding = 'utf-8'
    
        try:
            content = page.content
            save_output(Path(__file__).parent,beautify_html(content))
        except Exception as e:
            print(e)
            print(f'Unable to get DATA from {site} due to {e}')

if __name__ == "__main__":
    main()
