from .brand import Brand
from .utils import Color, Size, Media, DigiPlus, getIfExists
from .internet import Internet
from .seller import Market
from .review import ReviewCollection
from .question import QuestionCollection

class Product():
    def __init__(self, internet:Internet, data:dict, comments=False, question=False) -> None:
        self._internet = internet
        self.rawData = data
        self.id = data["product"]["id"]
        self.title = data["product"]["title_fa"]
        self.title_en = data["product"]["title_en"]
        self.status = data["product"]["status"]
        self.profileImge = Media(data["product"]["images"]["main"]["url"][0], data["product"]["images"]["main"]["url"][0], type_="image")
        self.images = self.__extractImages()
        self.rateCount = data["product"]["rating"]["count"]
        self.rate = data["product"]["data_layer"]["dimension9"]
        if getIfExists(data, "product", "colors"):
            self.colors = []
            for color in self.rawData["product"]["colors"]:
                self.colors.append(Color(color["title"], color["hex_code"]))
        self.videos = self.__extractVideos()
        self.returnAlart = self.__extractReturnAlart()
        self.brand = Brand(data["product"]["brand"])
        self.description = data["product"]["review"]["description"]
        self.attributes = self.__extractAttributes()
        self.prosAndCons = data["product"]["pros_and_cons"]
        self.suggestionCount = data["product"]["suggestion"]["count"]
        self.suggestionPercentage = data["product"]["suggestion"]["percentage"]
        self.questionCount = data["product"]["questions_count"]
        self.reviewCount = data["product"]["comments_count"]
        self.informations = data["product"]["specifications"][0]["attributes"]
        self.fullReview = getIfExists(data, "product", "expert_reviews", "review_sections")
        self.commentCollection = ReviewCollection(self, self._internet)
        self.questionCollection = QuestionCollection(self, self._internet)

        # geting first page of question and comments
        if comments:
            self.commentCollection.getReviewsPage(1)
        if question:
            self.questionCollection.getQuestionPage(1)

        # getting defautl market and price and if out of stock the default market will be None
        try:
            self.defaultMarket = Market(data["product"]["default_variant"])
            self.price = self.defaultMarket.price
            self.discount = self.defaultMarket.discountPercentage
        except KeyError:
            self.defaultMarket = None
        self.allMarkets = []

        # getting all markets if the product is not out of stock
        try:
            for i in data["product"]["variants"]:
                self.allMarkets.append(Market(i))
        except KeyError:
            pass

        self.digiPlus = DigiPlus(data["product"]["digiplus"])

        self.category = data["product"]["category"]["title_fa"]
        self.category_en = data["product"]["category"]["code"]
        self.categoryPipeLine = self.__extractCategoryPipeline(data["product"]["data_layer"])
        self.__specialOffer = data["product"]["data_layer"]["dimension7"]


    def __extractImages(self):
        imageList = []
        try:
            for i in self.rawData["product"]["images"]["list"]:
                imageList.append(Media(i["url"][0], i["url"][0], type_="image"))
        finally:
            return imageList

    def __extractVideos(self):
        videos = []
        try:
            for vid in self.rawData["product"]["videos"]:
                videos.append(Media(vid["url"], vid["cover"], type_="video"))
        finally:
            return videos

    def __extractAttributes(self):
        attrs = []
        try:
            for attr in self.rawData["product"]["review"]["attributes"]:
                attrs.append(attr)
        finally:
            return attrs
    
    def __extractReturnAlart(self):
        try:
            return self.rawData["product"]["category"]["return_reason_alert"]
        except:
            return ""
    
    def __extractAllMarkets(self, data):
        markets = []
        for i in data:
            markets.append(Market(i))
        
        return markets

    def __extractCategoryPipeline(self, data):
        c = []
        for i in ["item_category2", "item_category3", "item_category4", "item_category5"]:
            if data[i] != "":
                c.append(data[i])
        return c
    
    def isSpecialOffer(self):
        if self.__specialOffer != "":
            return True
        return False
