from .seller import Seller
from .utils import Media, Color, Size, getIfExists

class ReviewCollection():
    def __init__(self, product, internet) -> None:
        """
        download and manage reviews 
        """
        self._internet = internet
        self._product = product
        self.totalReviews = 0
        self.totalPages = 0
        self.reviewsCount = 0
        self.reviews = []
        self.generalViews = []
        self.media = []

    def __addReviews(self, data:list):
        """
        add reviews to reviews list!
        """
        self.reviewsCount += len(data)
        for r in data:
            self.reviews.append(Review(r))

    def __addMedias(self, data:list):
        """
        update reviews that have madia attached to them
        """
        if len(self.media) == len(data):
            return
        for r in data:
            self.media.append(Review(r))

    def __extractGeneralViewOptions(self, data:list):
        """
        extract all reviews static
        """
        self.generalViews.clear()
        for item in data:
            self.generalViews.append(GeneralViewOption(item))
    
    def getReviewsPage(self, page):
        """
        get a page of reviews and all reviews that have video or image attached to it
        alse updating total reviews and total pages and updating static of all reviews
        """
        if page > 100:
            print("only up to 100 page can be get!")
            return
        data = self._internet.getReviews(self._product.id, page)
        self.totalPages = data["pager"]["total_pages"]
        self.totalReviews = data["pager"]["total_items"]
        self.__extractGeneralViewOptions(data["intent_data"])
        if getIfExists(data, "comments"):
            self.__addReviews(data["comments"])
        if getIfExists(data, "media_comments"):
            self.__addMedias(data["media_comments"])

    def toCSV(self, path=None):
        if path and path[-4:] != ".csv":
            path = path + ".csv"
        if not path:
            path = "reviews.csv"
        with open(path, "w", encoding="utf8") as f:
            f.write(f"id,title,text,date,rate,likes,dislikes,recomendation,username,buyer,anonymous,advantages,disadvantages,seller ID,seller name\n")
            for item in self.media:
                f.write(f"\"{item.id}\",\"{item.title}\",\"{item.text}\",\"{item.date}\",\"{item.rate}\",\"{item.likes}\",\"{item.dislikes}\",\"{item.status}\",\"{item.name}\",\"{item.isBuyer()}\",\"{item.isAnonymous()}\",\"{item.advantages}\",\"{item.disadvantages}\"")
                if hasattr(item, "purchase"):
                    f.write(f",\"{item.purchase.seller.id}\",\"{item.purchase.seller.name}\"\n")
                else:
                    f.write(f",\"None\",\"None\"\n")
            for item in self.reviews:
                f.write(f"\"{item.id}\",\"{item.title}\",\"{item.text}\",\"{item.date}\",\"{item.rate}\",\"{item.likes}\",\"{item.dislikes}\",\"{item.status}\",\"{item.name}\",\"{item.isBuyer()}\",\"{item.isAnonymous()}\",\"{item.advantages}\",\"{item.disadvantages}\"")
                if hasattr(item, "purchase"):
                    f.write(f",\"{item.purchase.seller.id}\",\"{item.purchase.seller.name}\"\n")
                else:
                    f.write(f",\"None\",\"None\"\n")

            
class GeneralViewOption():
    def __init__(self, data:dict) -> None:
        """
        class for a product review static
        """
        self.title = data["title"]
        self.commentsCount = data["number_of_comments"]
        self.positive = data["tag_data"]["positive"]
        self.negative = data["tag_data"]["negative"]
        self.neutral = data["tag_data"]["neutral"]
        self.positivePercentage = data["tag_percentage"]["positive"]
        self.negativePercentage = data["tag_percentage"]["negative"]
        self.neutralPercentage = data["tag_percentage"]["neutral"]


class Review():
    def __init__(self, data) -> None:
        """
        review class for review with media and without
        """
        self.id = data["id"]
        self.title = getIfExists(data, "title")
        self.text = data["body"]
        self.date = data["created_at"]
        self.rate  = data["rate"]
        self.likes = data["reactions"]["likes"]
        self.dislikes = data["reactions"]["dislikes"]
        self.status = getIfExists(data, "recommendation_status")
        self.name = data["user_name"]
        self.__is_buyer = data["is_buyer"]
        self.__is_anonymous = data["is_anonymous"]
        self.hasMedia = False
        self.media = self.__extractMedia(data)
        self.advantages = getIfExists(data, "advantages")
        self.disadvantages = getIfExists(data, "disadvantages")
        if self.__is_buyer:
            self.purchase = Purchase(data["purchased_item"])

    def isBuyer(self):
        """
        is this review from a buyer or not (seller)
        """
        return self.__is_buyer

    def isAnonymous(self):
        """
        is person write the review logined or not (anonymous)
        """
        return self.__is_anonymous

    def __extractMedia(self, data:dict):
        """
        extract media from a review if have any
        """
        if "files" not in data.keys():
            return []
        
        medias = []
        self.hasMedia = True
        for media in data["files"]:
            medias.append(Media(media["url"][0], media["thumbnail_url"][0], code=media["storage_ids"][0]))
            
        return medias


class Purchase():
    def __init__(self, data) -> None:
        """
        class for information of a purchase
        """
        self.seller = Seller(data["seller"])
        if getIfExists(data, "color"):
            self.color = Color(data["color"]["title"], data["color"]["hex_code"])
        if getIfExists(data, "size"):
            self.size = Size(data["size"]["title"])