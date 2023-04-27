import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from DigiScraper import digikala

# can replce with any digikala url
url = "https://www.digikala.com/product/dkp-7579128/%D9%82%DB%8C%DA%86%DB%8C-%D8%A8%D8%A7%D8%BA%D8%A8%D8%A7%D9%86%DB%8C-%D8%B3%DB%8C-%D8%A2%DB%8C-%D8%A7%D8%B3-%D9%85%D8%AF%D9%84-sk-5/"
# url = "https://www.digikala.com/product/dkp-9727269/%D8%AE%D8%A7%DA%A9-%D8%A8%D9%86%D9%81%D8%B4%D9%87-%D8%B4%D8%B1%DA%A9%D8%AA-%DA%AF%D9%84%D8%A8%D8%A7%D8%B1%D8%A7%D9%86-%D8%B3%D8%A8%D8%B2-%DA%AF%DB%8C%D9%84%D8%A7%D9%86-%D9%85%D8%AF%D9%84-gpb-v7-%D9%88%D8%B2%D9%86-25-%DA%A9%DB%8C%D9%84%D9%88%DA%AF%D8%B1%D9%85/"

digi = digikala.DigiKala()
myProduct = digi.getProduct(url)

for i in range(1, 2):
    print(f"getting question in page {i}")
    myProduct.questionCollection.getQuestionPage(i)


print(f"{len(myProduct.questionCollection.questions)} reviews collected")
myProduct.questionCollection.toCSV()



