from .internet import Internet, API_SEARCH_WITH_CATEGORY_URL, API_SEARCH_WITHOUT_CATEGORY_URL, API_SEARCH_BASE_URL
from .suggestion import suggestionObj, suggestionType
from .product import ProductBanner
from .utils import getIfExists


class SortOption:
    def __init__(self, text:str, id:int) -> None:
        self.text = text
        self._id = id


class FilterType:
    Category = 0
    Switch = 1
    Slider = 2
    Checkbox = 3
    NestedList = 4
    Unknown = 5


class FilterOption:
    def __init__(self, key:str, id:str, type:FilterType, title:str, minValue:int=0, maxValue:int=0, isNested:bool=False) -> None:
        self.key:str = key
        self.id:str = id
        self.type:FilterType = type
        self.title:str = title
        self.minValue:int = minValue
        self.maxValue:int = maxValue


class FilterCollection:
    """
    a collection of filters that in one category like brands, colors, ...
    """
    def __init__(self, key:str, data:dict, isNested:bool=False) -> None:
        self._key:str = key   # key name for the collection that it will use to create filter in url
        self.title:str = data["title"]
        self.id:int = getIfExists(data, "id")  # id of the collection in nested List collection types
        self._options:list[FilterOption] = []   # all options in this collection that user can select to activate aas filter
        self.type:FilterType = FilterType.Unknown   # type of the filter e.g. switch, checkbox, ...

        if data["type"] == "nested_list":
            self.type = FilterType.NestedList
        elif data["type"] == "category_list":
            self.type = FilterType.Category
        elif data["type"] == "switch":
            self.type = FilterType.Switch
        elif data["type"] == "slider":
            self.type = FilterType.Slider
        elif data["type"] == "checkbox":
            self.type = FilterType.Checkbox

        if self.type != FilterType.NestedList:
            if self.type == FilterType.Slider:
                self._options.append(FilterOption(self.key(), "0", self.type, self.title, data["options"]["min"], data["options"]["max"], isNested))
            else:
                for option in data["options"]:
                    self._options.append(FilterOption(self.key(), str(option["id"]), self.type, self._getFilterOptionTitle(option), isNested=isNested))


    def _getFilterOptionTitle(self, filterOptionData:dict) -> str:
        if "title" in filterOptionData.keys():
            return filterOptionData["title"]
        elif "title_fa" in filterOptionData.keys():
            return filterOptionData["title_fa"]
        elif "title_en" in filterOptionData.keys():
            return filterOptionData["title_en"]
        return self.title
    
    def key(self):
        if self.type == FilterType.NestedList:
            return F"{self._key}[{self.id}]"
        return self._key
    
    def findFilterOptionByID(self, id:str) -> FilterOption|None:
        for option in self._options:
            if str(option.id) == str(id):
                return option
        return None
    
    def findFilterOptionByName(self, name:str) ->FilterOption|None:
        for option in self._options:
            if option.title == name:
                return option
        return None
    


class SearchEngine:
    def __init__(self, internetObject:Internet) -> None:
        self._internet:Internet = internetObject
        self.__baseUrlParamiters:dict = {}
        self.baseAPIUrl:str = ""
        self.defaultSortOption:SortOption|None = None
        self.sortOptions:list[SortOption] = None
        self.filetrCollections:list[FilterCollection] = None


    def _createBaseSearchUrl(self, searchObject:str|suggestionObj):
        if isinstance(searchObject, suggestionObj):
            if searchObject.type == suggestionType.Advance:
                # self.baseAPIUrl = API_SEARCH_BASE_URL + searchObject.url
                self.baseAPIUrl = API_SEARCH_WITH_CATEGORY_URL.replace("%CATEGORY", searchObject.code)

            elif searchObject.type == suggestionType.Trend:
                fullUrl = API_SEARCH_BASE_URL + searchObject.url
                self.baseAPIUrl = fullUrl.split("?")[0]

                # fill url paramiters e.g. 'q' or 'page'
                for i in fullUrl.split("?")[-1].split("&"):
                    splited = i.split("=")
                    if (len(splited) != 2):
                        raise ValueError(f"can't extract url paramiters")
                    self.__baseUrlParamiters[splited[0]] = splited[1]
            elif searchObject.type == suggestionType.withCategory:
                self.baseAPIUrl = API_SEARCH_WITH_CATEGORY_URL.replace("%CATEGORY", searchObject.code)
                self.__baseUrlParamiters["q"] = searchObject.keyword
            elif searchObject.type == suggestionType.Normal:
                self.baseAPIUrl = API_SEARCH_WITHOUT_CATEGORY_URL
                self.__baseUrlParamiters["q"] = searchObject.keyword
            else:
                raise TypeError("unknown suggestion type!")

        elif isinstance(searchObject, str):
            self.baseAPIUrl = API_SEARCH_WITHOUT_CATEGORY_URL
            self.__baseUrlParamiters["q"] = searchObject
        else:
            raise ValueError("search engine only accept string or suggestionObj type in searchObject ")

        self.__baseUrlParamiters["page"] = 1


    def _createSearchUrl(self, page:int, sortOption:SortOption|None, filterOptions:list[FilterOption]):
        self.__baseUrlParamiters["page"] = page
        url = self.baseAPIUrl + "?"
        # adding filter options to url
        url += self.parsFilterQuery(filterOptions)

        # adding base search paramiters
        for key in self.__baseUrlParamiters:
            url += f"&{key}={self.__baseUrlParamiters[key]}"

        # adding sort option to url
        if sortOption:
            if not self.defaultSortOption:
                url += f"&sort={sortOption._id}"
            else:
                if sortOption._id != self.defaultSortOption._id:
                    url += f"&sort={sortOption._id}"
        
        return url
    

    def parsFilterQuery(self, filterOptions:list[FilterOption]) -> str:
        if filterOptions == None:
            return ""
        
        url = ""
        counter = {}
        for filter in filterOptions:
            if filter:
                if filter.key in counter.keys():
                    counter[filter.key] += 1
                else:
                    counter[filter.key] = 0
                if filter.type == FilterType.Slider:
                    url += f"{filter.key}[max]={filter.maxValue}&{filter.key}[min]={filter.minValue}&"
                elif filter.type == FilterType.Switch:
                    url += f"{filter.key}=1&"
                else:
                    url += f"{filter.key}[{counter[filter.key]}]={filter.id}&"

        return url[:-1]

        
    
    def search(self, searchInput:suggestionObj|str, page:int = 1, sortOptions:SortOption|None = None, filterOptions:list[FilterOption] = []):
        if searchInput == "" and searchInput == None:
            raise ValueError("no search text is provided\n for search please provide a text input or suggestion object")

        self.__baseUrlParamiters.clear()
        self._createBaseSearchUrl(searchInput)
        url = self._createSearchUrl(page, sortOptions, filterOptions)
        print(url)
        rawData = self._internet.search(url)
        self.__result = SearchResult(rawData, self)
        
        # update filters and sort options
        self.defaultSortOption = self.__result.defaultSort
        self.sortOptions = self.__result.sortOptions
        self.filetrCollections = self.__result.filters
        return self.__result
    
    

    def selectSortOption(self, searchResult, id:int) -> SortOption|None:
        return searchResult.selectSortOption(id)


    def getFilterOptionByName(self, searchResult, name:str) -> FilterOption|None:
        return searchResult.findFilterOptionByName(name)

    def getFilterOptionByID(self, searchResult, id:str) -> FilterOption|None:
        return searchResult.findFilterOptionByID(id)


class SearchResult:
    def __init__(self, data:dict, engine:SearchEngine) -> None:
        self.__engine = engine
        self.currentPage:int = data["pager"]["current_page"]
        self.totalPages:int = data["pager"]["total_pages"]
        self.totalResults:int = data["pager"]["total_items"]

        self.products:list[ProductBanner] = []
        try:
            for p in data["products"]:
                self.products.append(ProductBanner(self.__engine._internet, p))
        except:
            pass

        self.filters:list[FilterCollection] = []
        for filter in data["filters"]:
            f = FilterCollection(filter, data["filters"][filter])
            if f.type == FilterType.NestedList:
                for nestedOption in data["filters"][filter]["options"]:
                    self.filters.append(FilterCollection(f.key(), nestedOption, True))
            else:
                self.filters.append(f)


        self.sortOptions:list[SortOption] = []
        self.defaultSort:SortOption = None
        for s in data["sort_options"]:
            self.sortOptions.append(SortOption(s["title_fa"], s["id"]))
            if self.sortOptions[-1]._id == int(data["sort"]["default"]):
                self.defaultSort = self.sortOptions[-1]

    def selectSortOption(self, id:int) -> SortOption|None:
        for i in self.sortOptions:
            if i._id == id:
                return i
        return None
    
    def findFilterOptionByName(self, name:str) -> FilterOption|None:
        for filterCollection in self.filters:
            f = filterCollection.findFilterOptionByName(name)
            if f != None:
                return f
        return None
    
    def findFilterOptionByID(self, id:str) -> FilterOption|None:
        for filterCollection in self.filters:
            f = filterCollection.findFilterOptionByID(id)
            if f != None:
                return f
        return None



def createSortOption(sortID:int, sortText:str="") -> SortOption:
    return SortOption(sortText, sortID)

def createFilter(id:int, type:FilterType, key:str, sliderMinvalue:int=0, sliderMaxValue:int=0, title:str="", title_en:str="", isNested:bool=False) -> FilterOption:
    return FilterOption(key, id, type, title, sliderMinvalue, sliderMaxValue, isNested)

def createPriceRangeFilter(minValue:int, maxValue:int) -> FilterOption:
    return FilterOption("price", "", FilterType.Slider , "price", minValue, maxValue)