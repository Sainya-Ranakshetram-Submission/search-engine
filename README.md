# Konohagakure Search
We were asked to do the following:
```
Develop an efficient Search Engine with the following features it should have distributed crawlers to crawl the private/air-gapped networks (data sources in these networks might include websites, files, databases) and must work behind sections of networks secured by firewalls

It should use AI/ML/NLP/BDA for better search (queries and results) It should abide by the secure coding practices (OWASP Top 10 and SANS Top 25 web vulnerability mitigation techniques.) feel free to improvise your solution and be creative with your approach Goal

Have a search engine which takes keyword/expression as an input and crawls the web (internal network or internet) to get all the relevant information. The application shouldn't have any vulnerabilities, make sure it complies with OWASP Top 10 Outcome Write a code which will scrape data, match it with the query and give out relevant/related information. Note - Make search as robust as possible (eg, it can correct misspelt query, suggest similar search terms, etc) be creative in your approach. Result obtained from search engine should display all the relevant matches as per search query/keyword along with the time taken by search engine to fetch that result There is no constraint on programming language.

To Submit: - A Readme having steps to install and run the application - Entire code repo - Implement your solution/model in Dockers only. - A video of the working search engine
```
## Building Docker Image
Just run 

```docker
docker build .
```
If you wish you can do teh necessary image tagging.

After building the image install the docker image.

## Hosting Guide (With the docker)
To run **Konohagakure Search** you need [python3.9](https://www.python.org/downloads/release/python-390/), latest version of [golang](https://go.dev/),
[postgres](https://www.postgresql.org/), [rabbitmq](https://www.rabbitmq.com/) and [redis](https://redis.io/)



```python
pip install --upgrade -r requirements.min.txt
```
```python
python -m spacy download en_core_web_md
python -m nltk.downloader stopwords
python -m nltk.downloader words
```

```go
go mod init crawler/crawler/spiders/subdomain_finder.go
go mod tidy
go build -o crawler/crawler/spiders/subdomain_finder.so -buildmode=c-shared ./crawler/crawler/spiders/subdomain_finder.go
```

```python
uvicorn search_engine.asgi:application --reload --lifespan off --host 0.0.0.0
```
