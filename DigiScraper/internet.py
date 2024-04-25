import requests
import json

DIGIKALA_URL = "https://www.digikala.com"
API_BASE_URL = "https://api.digikala.com/v2/product/"
API_COMMENT_URL = "https://api.digikala.com/v1/product/%ID/comments/?page=%PAGE"
API_QUESTION_URL = "https://api.digikala.com/v1/product/%ID/questions/?page=%PAGE"
API_SUGGESTION_URL = "https://api.digikala.com/v1/autocomplete/?q=%TEXT"
API_SEARCH_BASE_URL = "https://api.digikala.com/v1"
API_SEARCH_WITH_CATEGORY_URL = API_SEARCH_BASE_URL + "/categories/%CATEGORY/search/"
API_SEARCH_WITHOUT_CATEGORY_URL = API_SEARCH_BASE_URL + "/search/"

class Internet():
    def __init__(self) -> None:
        """
        managing all json download from digikala api
        """
        self._session = requests.Session()
        _baseHeader = {'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
                        'Accept': 'application/json, text/plain, */*',
                        'X-Web-Client': 'desktop',
                        'Sec-Ch-Ua-Mobile': '?0',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36',
                        'X-Web-Optimize-Response': '1',
                        'Sec-Ch-Ua-Platform': '"Windows"',
                        'Origin': 'https://www.digikala.com',
                        'Sec-Fetch-Site': 'same-site',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Dest': 'empty',
                        'Referer': 'https://www.digikala.com/',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.9'}
        self._session.headers.update(_baseHeader)


    def getGeneralInfo(self, url:str) -> dict:
        """
        downloading full pruduct info
        """
        serialNumber = Internet.extractProductNumber(url)
        url = API_BASE_URL+serialNumber+"/"
        res = self._session.get(url)
        if res.ok:
            return json.loads(res.text)["data"]
        else:
            return {}

    def getReviews(self, id, page=1) -> dict:
        """
        download a page of reviews and all reviews with media attached and all review static
        """
        url = API_COMMENT_URL.replace("%ID", str(id)).replace("%PAGE", str(page))
        res = self._session.get(url)
        if res.ok:
            return json.loads(res.text)["data"]
        else:
            return {}

    
    def getQuestions(self, id, page) -> dict:
        """
        download a page of question with answers
        """
        url = API_QUESTION_URL.replace("%ID", str(id)).replace("%PAGE", str(page))
        res = self._session.get(url)
        if res.ok:
            return json.loads(res.text)["data"]
        else:
            return {}

    
    def search(self, url:str):
        """
        get the produsts when searching text
        every page is contain 20 product
        """
        res = self._session.get(url)
        if res.ok:
            return json.loads(res.text)["data"]
        else:
            return {}
        


    def getSuggestions(self, text:str):
        """
        get digikala search suggestions
        """
        url = API_SUGGESTION_URL.replace("%TEXT", text)
        res = self._session.get(url)
        if (res.ok):
            return json.loads(res.text)["data"]
        else:
            return {}
        

    @staticmethod
    def extractProductNumber(text:str) -> str:
        """
        extract product serial number from a product url
        """
        #https://www.digikala.com/product/dkp-5987991/
        subUrls = text.split("/")
        for p in subUrls:
            if p[:4] == "dkp-":
                return p[4:]
    
    @staticmethod
    def getMedia(url):
        res = requests.get(url)
        if res.ok:
            return res.content
        return None
