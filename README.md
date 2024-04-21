# digiScraper

A scraper to crawler digikala pages, sellers, comments and questions
with this scraper you can scrape pages of digikala by passing corresponding url and get all info of that page.

some capability of this scraper is:
* All sellers of a pruduct with thier prices, ranks, rates, ...
* Default seller with default price .
* all official images and videos and all images and videos of buyers.
* all Specifications of product.
* All commects (reviews) up to 100 page.
* All questions about product with the answers.
* Full static of the product such as collers, full rating system, stars and ...
* Builtin function to get .csv output for reviews and questions.

# How to use

1. fist of first install `python`from official website.
2. then clone the repository with command below.
```bash
$ git clone https://github.com/belaboluk/digiScraper.git
```
3. copy the `/src` directory to your main python code.
4. import `digikala.py` to the main python file.
5. use `DigiKala` class in `digikala.py` to create a instance.
```python
# main python file
from digikala import DigiKala
digi = DigiKala()
page = digi.getProduct(url)
```
6. use the `page` attrebutes to extract what you want. :smile:

# Dependences

this scraper only require `requests` module that can installed via command below:
```bash
$ pip install requests
```

## Examples

i added 4 example for getting overall view of a product, question, commects(reviews) and all sellers  info in example folder

