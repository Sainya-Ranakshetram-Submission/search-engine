# Konohagakure Search
We were asked to do the following:
```
Develop an efficient Search Engine with the following features it should have distributed crawlers to crawl the private/air-gapped networks (data sources in these networks might include websites, files, databases) and must work behind sections of networks secured by firewalls

It should use AI/ML/NLP/BDA for better search (queries and results) It should abide by the secure coding practices (
 and SANS Top 25 web vulnerability mitigation techniques.) feel free to improvise your solution and be creative with your approach Goal

Have a search engine which takes keyword/expression as an input and crawls the web (internal network or internet) to get all the relevant information. The application shouldn't have any vulnerabilities, make sure it complies with OWASP Top 10 Outcome Write a code which will scrape data, match it with the query and give out relevant/related information. Note - Make search as robust as possible (eg, it can correct misspelt query, suggest similar search terms, etc) be creative in your approach. Result obtained from search engine should display all the relevant matches as per search query/keyword along with the time taken by search engine to fetch that result There is no constraint on programming language.

To Submit: - A Readme having steps to install and run the application - Entire code repo - Implement your solution/model in Dockers only. - A video of the working search engine
```

## Features
- Corrected Spelling suggestions
- Auto Suggested
- 3 different types of crawler
- Distributed crawlers
- A site submit form
- Blazingly fast
And so on...

## Vulnerabilities the application that it address
It address the following [SANS Top 25 Most Dangerous Software Errors](https://www.sans.org/top25-software-errors/) and [OWASP Top 10 Vulnerabilities](https://www.veracode.com/security/owasp-top-10)

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging and Monitoring
11. Improper Restriction of Operations within the Bounds of a Memory Buffer
12. Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
13. Improper Input Validation
14. Information Exposure
15. Out-of-bounds Read
16. Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
17. Use After Free
18. Integer Overflow or Wraparound
19. Cross-Site Request Forgery (CSRF)
20. Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
21. Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
22. Out-of-bounds Write
23. Improper Authentication
24. NULL Pointer Dereference
25. Incorrect Permission Assignment for Critical Resource
26. Unrestricted Upload of File with Dangerous Type
27. Improper Restriction of XML External Entity Reference
28. Improper Control of Generation of Code ('Code Injection')
29. Use of Hard-coded Credentials
30. Uncontrolled Resource Consumption
31. Missing Release of Resource after Effective Lifetime
32. Untrusted Search Path
33. Deserialization of Untrusted Data
34. Improper Privilege Management
35. Improper Certificate Validation

## Building Docker Image
Just run 

```docker
docker build .
```
Also check this [out](https://stackoverflow.com/questions/59608788/unable-to-start-docker-desktop-on-windows-10)
If you wish you can do teh necessary image tagging.

After building the image install the docker image.

## Hosting Guide (without the docker)
To run **Konohagakure Search** you need [python3.9](https://www.python.org/downloads/release/python-390/), latest version of [golang](https://go.dev/),
[postgres](https://www.postgresql.org/), [rabbitmq](https://www.rabbitmq.com/) and [redis](https://redis.io/)

See their installation instruction and download it properly.

After downloading the above mentioned softwares, now run the following commands in console after opening the terminal:

#### 1. Clone the repository
Clone the repository using git
```git
git clone https://github.com/Sainya-Ranakshetram-Submission/search-engine.git
```
#### 2. Install the virtual environment
```python
pip install --upgrade virtualenv
cd search-engine
virtualenv env
env/scripts/activate
```
#### 3. Install the dependencies
```python
pip install --upgrade -r requirements.min.txt
```
```python
python -m spacy download en_core_web_md
python -m nltk.downloader stopwords
python -m nltk.downloader words
```
```go
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```
#### 4. Setup the environment variables
Rename the [example.env](https://github.com/Sainya-Ranakshetram-Submission/search-engine/blob/master/example.env) to `.env` and setup the environment variables according to your choice.

#### 5. Create a database
Now open `pgadmin` and create a database named `search_engine`. After creating the database reassign the `DATABASE_URL` value acordingly in `.env` file.
Note please read this [also](https://github.com/jacobian/dj-database-url#url-schema)

#### 6. Start Rabitmq and Redis Instance
Read their docs regarding how to start them. [redis](https://redis.io/documentation) [rabbitmq](https://rabbitmq.com/documentation.html)

#### 7. Migrate the data
```python
python manage.py migrate
```

And to migrate the 10 Lakh dataset of the website for the crawler to crawl, do
```python
python manage.py migrate_default_to_be_crawl_data
```
I have also given some crawled datasets for the reference, you can see it here [data_backup](https://github.com/Sainya-Ranakshetram-Submission/search-engine/blob/master/data_backup)

#### 8. Create a superuser for the site
```python
python manage.py createsuperuser
```
It asks for some necessary information, give it then it will create a superuser for the site.

#### 9. Running the celery worker and beat
Now run this command in ther terminal
```python
python manage.py add_celery_tasks_in_panel
```
Now, open two different terminals
And run these commands respectively :-
```celery
celery -A search_engine worker --loglevel=INFO
```
```celery
celery -A search_engine beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

#### 10. Run the application
- For `windows`, `mac-os`, `linux`

Without IP address bound
```console
    uvicorn search_engine.asgi:application --reload --lifespan off
```

IP address bound
```console
     uvicorn search_engine.asgi:application --reload --lifespan off --host 0.0.0.0
```

If you are `Linux` then you can run this command also instead of the above one:
```console
    gunicorn search_engine.asgi:application -k search_engine.workers.DynamicUvicornWorker --timeout 500
```

## Python custom commands reference
- `add_celery_tasks_in_panel` : Add the celery tasks to the django panel
- `crawl_already_crawled` : Scraps already scrapped/crawled sites in database
- `crawl_to_be_crawled` : Scraps newly entered sites in database || The sites that needs to be crawled ||
- `migrate_default_to_be_crawl_data` : Enters BASE data of the websites that needs to be crawled, its about 10 Lakh sites

## Distributed Crawlers
For the distributed web crawlers refer to the following [scrapy documentation link](https://docs.scrapy.org/en/latest/topics/practices.html#distributed-crawls)

## Running crawler manually from command line
There are 3 different ways in order to achieve this

#### 1. crawl_already_crawled
This is custom django management command and it starts crawling the already crawled and stored sites and then updates it
```python
python manage.py crawl_already_crawled
```

#### 2. crawl_to_be_crawled
This is custom django management command and it starts crawling the site which were entered using either the `migrate_default_to_be_crawl_data` custom command or it was entered using `submit_site/` endpoint
```python manage.py crawl_to_be_crawled
```

#### 3. Scrapy Command Line Crawler
This is a scrapy project that crawls the site using the command line
Here in `example.com` replace it with the site you want to crawl (without `http` or https`)
```scrapy
scrapy crawl konohagakure_to_be_crawled_command_line -a allowed_domains=example.com
```

![Minato Namikaze Konohagakure Yondaime Hokage](https://i.imgur.com/WrNbHOT.jpeg "Minato Namikaze")
