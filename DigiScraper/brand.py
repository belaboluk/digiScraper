DIGIKALA_BASE_URL = "https://www.digikala.com"

class Brand():
    def __init__(self, data:dict) -> None:
        self.id = data["id"]
        self.name = data["code"]
        self.name_fa = data["title_fa"]
        self.name_en = data["title_en"]
        self.pageUrl = Brand.__extractUrl(data["url"])
        self.logo = data["logo"]["url"][0]
        self.isVisible = data["visibility"]
        self.isPremium = data["is_premium"]
        self.isMiscellaneous = data["is_miscellaneous"]
        self.nameIsSimilar = data["is_name_similar"]

    @staticmethod
    def __extractUrl(url):
        """
        getting url 
        it can be url or uri!
        """
        if type(url) == str:
            return url
        elif type(url) == dict and "uri" in url.keys():
            return DIGIKALA_BASE_URL + url["uri"].replace("\/", "/")