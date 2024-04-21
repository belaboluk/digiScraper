from .utils import Color, Size, DigiPlus, getIfExists

DIGIKALA_BASE_URL = "https://www.digikala.com"

class Seller():
    def __init__(self, data) -> None:
        """
        class to manage seller infos
        used in reviews and shops
        """
        self.id = data["id"]
        self.name = data["title"]
        self.code = data["code"]
        self.pageUrl = Seller.__extractUrl(data["url"])

        # in coments response star and membersip is not sended
        try:
            self.stars = data["stars"]
        except:
            self.stars = None
        try:
            self.membership = data["registration_date"]
        except:
            self.membership = None

        # in question response rating and properties is not sended
        try:
            self.rate = data["rating"]["total_rate"]
            self.rateCount = data["rating"]["total_count"]
            self.commitment = data["rating"]["commitment"]
            self.noReturn = data["rating"]["no_return"]
            self.onTimeShipping = data["rating"]["on_time_shipping"]
        except:
            self.rate = None
            self.rateCount = None
            self.commitment = None
            self.noReturn = None
            self.onTimeShipping = None
        try:
            self.trusted = data["properties"]["is_trusted"]
            self.official = data["properties"]["is_official"]
            self.roosta = data["properties"]["is_roosta"]
            self.isNew = data["properties"]["is_new"]
        except:
            self.trusted = None
            self.official = None
            self.roosta = None
            self.isNew = None

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


class Market():
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.leadTime = data["lead_time"]
        self.rank = data["rank"]
        self.rate = data["rate"]
        self.fullSatisfiedCustomerCount = getIfExists(data, "statistics", "totally_satisfied", "rate_count")
        self.fullSatisfiedCustomerRate = getIfExists(data, "statistics", "totally_satisfied", "rate")
        self.satisfiedCustomerCount = getIfExists(data, "statistics", "satisfied", "rate_count")
        self.satisfiedCustomerRate = getIfExists(data, "statistics", "satisfied", "rate")
        self.neutrlCustomerCount = getIfExists(data, "statistics", "neutral", "rate_count")
        self.neutrlCustomerRate = getIfExists(data, "statistics", "neutral", "rate")
        self.dissatisfiedCustomerCount = getIfExists(data, "statistics", "dissatisfied", "rate_count")
        self.dissatisfiedCustomerRate = getIfExists(data, "statistics", "dissatisfied", "rate")
        self.fullDissatisfiedCustomerCount = getIfExists(data, "statistics", "totally_dissatisfied", "rate_count")
        self.fullDissatisfiedCustomerRate = getIfExists(data, "statistics", "totally_dissatisfied", "rate")
        self.rateCount = getIfExists(data, "statistics", "total_count")
        self.status = data["status"]
        self.__isFastShipping = data["properties"]["is_fast_shipping"]
        self.__isShipBySeller = data["properties"]["is_ship_by_seller"]
        self.__isMultiWarehouse = data["properties"]["is_multi_warehouse"]
        self.__isSimilarMarket = data["properties"]["has_similar_variants"]
        self.__isRural = data["properties"]["is_rural"]
        self.__isDigikalaWarehouse = data["properties"]["in_digikala_warehouse"]
        
        self.digiPlus = DigiPlus(data["digiplus"])
        
        self.warrantyId = data["warranty"]["id"]
        self.warrantyTitle = data["warranty"]["title_fa"]
        self.warrantyTitleEn = data["warranty"]["title_en"]
        if getIfExists(data, "color"):
            self.color = Color(data["color"]["title"], data["color"]["hex_code"])
        if getIfExists(data, "size"):
            self.size = Size(data["size"]["title"])
        self.seller = Seller(data["seller"])
        self.digiclubPoint = data["digiclub"]["point"]

        self.price = data["price"]["selling_price"]
        self.priceWithoutDiscount = data["price"]["rrp_price"]
        self.orderLimit = data["price"]["order_limit"]
        self.__isIncredible = data["price"]["is_incredible"]
        self.__isPromotion = data["price"]["is_promotion"]
        self.__isLockedForDigiplus = data["price"]["is_locked_for_digiplus"]
        self.discountPercentage = data["price"]["discount_percent"]

        self.shipment = data["shipment_methods"]["description"]
        self.sellersShipment = self.__extractSellerShipment(data["shipment_methods"]["providers"])





    def __extractSellerShipment(self, providers):
        result = []
        for i in providers:
            result.append([i["title"], i["description"], i["type"]])
        return result

    def isFastShipping(self):
        return self.__isFastShipping

    def isShipBySeller(self):
        return self.__isShipBySeller

    def isMultiWarehouse(self):
        return self.__isMultiWarehouse

    def isSimilarMarket(self):
        return self.__isSimilarMarket

    def isRural(self):
        return self.__isRural

    def isDigikalaWarehouse(self):
        return self.__isDigikalaWarehouse

    def isIncredible(self):
        return self.__isIncredible

    def isPromotion(self):
        return self.__isPromotion

    def isLockedForDigiplus(self):
        return self.__isLockedForDigiplus
