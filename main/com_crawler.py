from typing import Optional, Union
from django.utils.html import strip_tags
from bs4 import BeautifulSoup


import cdx_toolkit
import spacy
import nltk
import requests
from nltk.corpus import stopwords
from functools import lru_cache
from nltk.tokenize import word_tokenize

cdx = cdx_toolkit.CDXFetcher(source='cc')
nlp = spacy.load("en_core_web_md")
stop_words = set(stopwords.words('english'))

@lru_cache
def crawl(url: str, limit: Optional[int] = 10) -> Optional[str]:
    url = f'{url}/*'
    for obj in cdx.iter(url, limit=limit):
        try:
            return obj.content.decode()
        except:
            return None

def requests_crawl(url: str) -> Optional[str]:
    url = f'https://{url}'
    try:
        return requests.get(url).text
    except:
        return None

@lru_cache
def keywords_gen_and_rank(body: str):
    doc = nlp(body)
    keywords = list(doc.ents)
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

@lru_cache
def formatter(content: str) -> dict:
    return_dict={}
    def remove_tags(html: str):
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script','noscript']):
            data.decompose()
        return ' '.join(soup.stripped_strings)
    soup = BeautifulSoup(content, 'html.parser')
    try:
        title = soup.find('title')
        return_dict.update({'title': title.getText()})
    except:
        pass
    try:
        description_site = soup.find('body')
        doc = nlp(description.getText())
        keywords_in_site=list(doc.ents)
        return_dict.update({
            'keywords_in_site':keywords_in_site,
            'stripped_request_body': description_site.getText(),
            'keywords_ranking': keywords_gen_and_rank(description_site.getText())
        })
    except:
        pass
    try:
        description_meta = soup.find('meta', description=True)
        return_dict.update({'stripped_request_body': description_meta.getText()})
    except:
        pass
    return return_dict