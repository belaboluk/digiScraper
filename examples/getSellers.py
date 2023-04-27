import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from DigiScraper import digikala

# can replce with any digikala url
url = "https://www.digikala.com/product/dkp-5856710/%D9%87%D8%AF%D9%81%D9%88%D9%86-%D8%A8%D9%84%D9%88%D8%AA%D9%88%D8%AB%DB%8C-%DA%A9%DB%8C%D9%88-%D8%B3%DB%8C-%D9%88%D8%A7%DB%8C-%D9%85%D8%AF%D9%84-t13-tws/"
# url = "https://www.digikala.com/product/dkp-3297174/%D9%82%DB%8C%DA%86%DB%8C-%D8%A8%D8%A7%D8%BA%D8%A8%D8%A7%D9%86%DB%8C-%D8%B3%DB%8C-%D8%A2%DB%8C-%D8%A7%D8%B3-%D9%85%D8%AF%D9%84-%D8%A7%D8%B320/"
# url = "https://www.digikala.com/product/dkp-9727269/%D8%AE%D8%A7%DA%A9-%D8%A8%D9%86%D9%81%D8%B4%D9%87-%D8%B4%D8%B1%DA%A9%D8%AA-%DA%AF%D9%84%D8%A8%D8%A7%D8%B1%D8%A7%D9%86-%D8%B3%D8%A8%D8%B2-%DA%AF%DB%8C%D9%84%D8%A7%D9%86-%D9%85%D8%AF%D9%84-gpb-v7-%D9%88%D8%B2%D9%86-25-%DA%A9%DB%8C%D9%84%D9%88%DA%AF%D8%B1%D9%85/"

digi = digikala.DigiKala()
myProduct = digi.getProduct(url)

print(f"{myProduct.title} have {len(myProduct.allMarkets)} market")
if myProduct.status != "marketable":
    print(f"{myProduct.title} is not avalable!")
    sys.exit()

print(f"default market is {myProduct.defaultMarket.seller.name} with price of {myProduct.defaultMarket.price} ({myProduct.defaultMarket.discountPercentage} discount)")
for m in myProduct.allMarkets:
    print(f"\t{m.seller.name}")
    print(f"\t\tprice: {m.price}   {m.discountPercentage}% discount")
    print(f"\t\trate: {m.rate}")
    print(f"\t\trank: {m.rank}")
    print(f"\t\tfull satisfaction customer: {m.fullSatisfiedCustomerCount} ({m.fullSatisfiedCustomerRate}%)\
            \n\t\tsatisfied customer: {m.satisfiedCustomerCount} ({m.satisfiedCustomerRate}%)\
            \n\t\tneutrl customer: {m.neutrlCustomerCount} ({m.neutrlCustomerRate}%)\
            \n\t\tdissatisfied customer: {m.dissatisfiedCustomerCount} ({m.dissatisfiedCustomerRate}%)\
            \n\t\tull Dissatisfied customer: {m.fullDissatisfiedCustomerCount} ({m.fullDissatisfiedCustomerRate}%)")
    print(f"\t\twaranty: {m.warrantyTitle}")

