from .internet import Internet
from .product import Product
from .suggestion import parsSuggestions, suggestionObj
from .searchEngine import SearchEngine, SearchResult, SortOption, FilterOption

class DigiKala():
    def __init__(self) -> None:
        self._internet = Internet()
        self._searchEngine = SearchEngine(self._internet)
        

    def getProduct(self, url:str, comments=False, question=False):
        rawData = self._internet.getGeneralInfo(url)
        product = Product(self._internet, rawData, comments=comments, question=question)
        return product

    def search(self, searchInput:suggestionObj|str, page:int = 1, sortOptions:SortOption|None = None, filterOptions:list[FilterOption] = []) -> SearchResult:
        return self._searchEngine.search(searchInput, page, sortOptions, filterOptions)

    def getSuggestions(self, text:str) -> list[suggestionObj]:
        rawData = self._internet.getSuggestions(text)
        return parsSuggestions(rawData)