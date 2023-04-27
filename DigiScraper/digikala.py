from .internet import Internet
from .product import Product

class DigiKala():
    def __init__(self) -> None:
        self._internet = Internet()
        

    def getProduct(self, url:str, comments=False, question=False):
        rawData = self._internet.getGeneralInfo(url)
        product = Product(self._internet, rawData, comments=comments, question=question)
        return product