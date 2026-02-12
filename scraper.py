import requests
import os
import nltk
import time
from ddgs import DDGS
from ollama import chat
from pathlib import Path
from trends import Trend
from bs4 import BeautifulSoup
from plyer import notification
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.parsers.plaintext import PlaintextParser

class Prompt():
    def __init__(self):
        pass

    def format_summary(self):
        cmd = """Take the provided context and content. Create a clean, concise summary. 
                    - Remove fluff and repetition
                    - Focus only on key points  
                    - Use direct, professional language
                    - Maximum 5-6 sentences
                    - Add somthing if you think that the additional stuff is needed
            """
        return cmd

    def top_topic(self,topics):

        topics_str = ", ".join(str(topic) for topic in topics)

        cmd = f'''TOPICS: {topics_str}

PICK ONE TOPIC ONLY.
OUTPUT FORMAT: 
"<topic_name>"

RULE 1: ONLY the topic name between quotes
RULE 2: NO explanations  
RULE 3: NO other text

"Quantum Computing Breakthroughs"'''

        return cmd

    def X_post(self,summary):
        cmd = f'''Create an X (Twitter) post based on this SUMMARY: {summary}

Guidelines:
- Max 200 characters (strict limit)
- Minimal emojis (0-1 max, only if they add value)
- Proper line spacing for readability
- Clean, focused for X audience: concise, punchy, insightful
- Highlight 1 key takeaway or unique angle
- Public persona: wise, value-driven, sparks curiosity
- End with subtle CTA or question

Output only the final post + character count. No extras.
'''
        return cmd


class Location:
    def __init__(self):
        pass
    
    def output_locate(self):
        OUTPUT_FILE = os.path.join(Path(__file__).parent,'output.txt') 
        return OUTPUT_FILE
    
    def summary_locate(self):
        SUMMARY_FILE = os.path.join(Path(__file__).parent,'summary.txt')
        return SUMMARY_FILE

    def post(self,of):
        X_FILE = os.path.join(Path(__file__).parent,'post','X.txt')
        LINKEDIN_FILE = os.path.join(Path(__file__).parent,'post','LinkedIn.txt')
        if of.lower() == 'x':
            return X_FILE
        elif of.lower() == 'linkedin':
            return LINKEDIN_FILE
        
        raise Exception('Posting platform not found') 
    
class Create_Post:
    def __init__(self):
        pass

    def X(self,summary):
        response = load_model(model,prompt.X_post(summary))
        return response
    
    def LinkedIn(self):
        return "Creating LinkedIn post"

loc = Location()
prompt = Prompt()
post = Create_Post()
model = 'phi'

def init():
    loc = Location()

    if os.path.exists(loc.output_locate()):
        os.remove(loc.output_locate())
    
    if os.path.exists(loc.summary_locate()):
        os.remove(loc.summary_locate())

    if os.path.exists(loc.post('x')):
        os.remove(loc.post('x'))

    if not os.path.exists(os.path.join(os.getcwd(),'post')):
        os.mkdir('post')
    
    return 0

def read_output():
    with open(loc.output_locate(),'r',encoding='utf-8') as f:
        content = f.read()
    return content

def save_data(location,data):
    with open(location,'a',encoding='utf-8') as f:
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

def scrape_sites(search_for):
    sites = relevant_sites(search_about=search_for)
    for site in sites:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        page = requests.get(site, headers=headers, timeout=10)
        page.encoding = 'utf-8'
    
        try:
            content = page.content
            save_data(loc.output_locate(),beautify_html(content))
        except Exception as e:
            print(e)
            print(f'Unable to get DATA from {site} due to {e}')

def summary():

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

    ARTICLE = read_output()
    LANGUAGE = "english"
    SENTENCES_COUNT = 5

    parser = PlaintextParser(ARTICLE, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LuhnSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = summarizer(parser.document, SENTENCES_COUNT)

    summary_ = ' '.join(str(sentence) for sentence in summary)
    save_data(loc.summary_locate(),summary_)
    return summary_

def load_model(model_name,prompt):

    response = chat(
        model=model_name,
        messages=[{'role': 'system', 'content': f"{prompt}"}]
    )

    result = response.message.content
    return result

def trending(keyword):
    trend = Trend()
    trend.analyze_trends(keyword)
    topics = trend.get_related_topics(keyword)

    response = load_model(model,prompt.top_topic(topics))
    return response


def send_notification(title,msg):
    notification.notify(            #type: ignore
        title=title,
        message=msg,
        timeout=5,
        app_name="Post Automation"
    )

def main():
    today_topic = str(input('Enter any key word : '))

    best_topic = trending(today_topic)
    send_notification('Best topic found','Model response has been generated..')
    print(f"Best Topic reccomendation by phi : {best_topic}")
    
    search_for = str(input('Want to search about : '))
    scrape_sites(search_for)
    send_notification('Web Scraping completed','Web scraping has been done..')

    summary_response = load_model(model,f"Topic: {search_for}\n\n-Summary:\n{summary()}\n\nInstructions:\n{prompt.format_summary()}\n\nReturn ONLY the new summary:")
    save_data(loc.summary_locate(),summary_response)
    send_notification('Summary generation Done.','Summary generation has been done..')

    print(f'Summary saved into {loc.summary_locate()}')
    send_notification('Creating Post.','Creating post for X..')
    print('Creating X post..')
    X_post = post.X(summary_response)
    send_notification('X post created.','X post has been generated..')
    save_data(loc.post('x'),X_post)
    

if __name__ == "__main__":
    init()
    main()