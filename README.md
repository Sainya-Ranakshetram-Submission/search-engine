# search-engine
Google Like Search Engine

# Please don't make any PR to this repo!

```python
pip install rcssmin==1.0.6 --install-option="--without-c-extensions"
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
uvicorn search_engine.asgi:application --reload --lifespan off
```
