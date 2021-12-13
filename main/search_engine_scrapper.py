from bs4 import BeautifulSoup
from requests import get, utils
from typing import Optional
from functools import lru_cache
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from crawler.common_user_agent import return_random_user_agent
from .models import CrawledWebPages

@lru_cache
def search(term: str, num_results: Optional[int] = 15, lang: Optional[str] = "en", proxy=None) -> list:
    headers = utils.default_headers()
    headers.update(
        {
            'User-Agent': return_random_user_agent(),
        }
    )
    def fetch_results(search_term, number_results, language_code):
        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(
            escaped_search_term, 
            number_results+1,
            language_code
        )
        proxies = None
        if proxy:
            if proxy[:5]=="https":
                proxies = {"https":proxy} 
            else:
                proxies = {"http":proxy}
        response = get(google_url, headers=headers, proxies=proxies)
        return response.text
    
    def keywords_gen_and_rank(body: str):
        nlp = spacy.load("en_core_web_md")
        doc = nlp(body)
        keywords = list(doc.ents)
        
        stop_words = set(stopwords.words('english'))
        tf_score = {}
        for each_word in body.split():
            each_word = each_word.replace('.','')
            if each_word not in stop_words:
                if each_word in tf_score:
                    tf_score[each_word] += 1
                else:
                    tf_score[each_word] = 1
        tf_score.update((x, y/int(len(body.split()))) for x, y in tf_score.items())
        keyword_ranking=tf_score
        return keywords, keyword_ranking

    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            description_soup = BeautifulSoup(str(result), 'html.parser')
            description = description_soup.find('div', attrs={'class': 'VwiC3b'})
            if link and title:
                try:
                    keywords_data = keywords_gen_and_rank(description.getText())
                except:
                    keywords_data = []
                model = CrawledWebPages(
                    url=link['href'], 
                    keywords_ranking=keywords_data[-1] if keywords_data else keywords_data,
                    keywords_in_site=keywords_data[0] if keywords_data else keywords_data
                )
                try:
                    model.title = title.getText()
                except:
                    pass
                try:
                    model.stripped_request_body=description.getText()
                except:
                    pass
                try:
                    model.save()
                except:
                    pass
                yield model

    html = fetch_results(term, num_results, lang)
    return list(parse_results(html))


