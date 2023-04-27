import os
from .internet import Internet

IMAGE_PREFIX = [".jpg", ".jpe", ".png"]
VIDEO_PREFIX  = [".mp4", ".mov"]

class Color():
    def __init__(self, name, hex) -> None:
        self.name = name
        self.hex = hex


class Size():
    def __init__(self, size) -> None:
        self.size = size

class downloadable():
    def __download(self, url, path=None, fileName = None):
        """
        download the media
        """
        # check if the path is filled and exists
        if not path:
            path = os.getcwd() + f"{os.sep}media"
        
        if not os.path.exists(path):
            os.makedirs(path)

        name = self._findFileName()
        if not fileName:
            fileName = name
        else:
            if "." not in fileName:
                prefix = name.split(".")[-1]
                fileName = fileName + f".{prefix}"

        content = Internet.getMedia(url)
        if content:
            with open(os.path.join(path, fileName), "wb") as f:
                f.write(content)
        else:
            print(f"[ERR] cann't download media in {url}")

    def download(self, path=None, fileName = None):
        if hasattr(self, "url"):
            self.__download(self.url, path, fileName)
        else:
            print("object has no url attribute")


    def downloadThumbnail(self, path=None, fileName = None):
        if hasattr(self, "thumbnail"):
            self.__download(self.thumbnail, path, fileName)
        else:
            print("object has no thumbnail attribute")

    def _findFileName(self) -> str:
        p = self.url.split("/")
        for i in p[3:]:
            if "." in i:
                return i.split("?")[0]

                    
class Media(downloadable):
    def __init__(self, url:str, thumbnail:str, type_=None, code=None) -> None:
        """
        class for official and buyer images and videos 
        saving url of souorce and thumbnail of media 
        """
        self.url = url
        self.thumbnail = thumbnail
        
        if type_ in ["image", "video"]:
            self.type = type_
        elif code != None:
            loc = url.find(code) + len(code)
            prefix = url[loc:loc+4]
            if prefix.lower() in IMAGE_PREFIX:
                self.type = "image"
            elif prefix.lower() in VIDEO_PREFIX:
                self.type = "video"
            else:
                print(f"Unknow media type! -> {self.url}")
                self.type = "unknown"


class DigiPlus():
    def __init__(self, data) -> None:
        self.services = getIfExists(data, "services")
        self.__isJet = getIfExists(data, "is_jet_eligible")
        self.moneyBack = getIfExists(data, "cash_back")
        self.__isJetInGeneralLocation = getIfExists(data, "is_general_location_jet_eligible")
        self.fastShippingText = getIfExists(data, "fast_shipping_text")

    def isJet(self):
        return self.__isJet
    
    def isJetInGeneralLocation(self):
        return self.__isJetInGeneralLocation


def getIfExists(data, *arg):
    if len(arg) == 1:
        try:
            return data[arg[0]]
        except:
            return None
    elif len(arg) == 2:
        try:
            return data[arg[0]][arg[1]]
        except:
            return None
    elif len(arg) == 3:
        try:
            return data[arg[0]][arg[1]][arg[2]]
        except:
            return None
    else:
        raise IndexError("TOO DEAPE!")