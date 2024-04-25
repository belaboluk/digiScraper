from .utils import getIfExists

class suggestionType:
    withCategory = 0
    Normal = 1
    Advance = 2
    Trend = 3


class suggestionObj:
    def __init__(self, key:str, data:dict) -> None:
        self.keyword:str = data["keyword"]
        self.category:str = getIfExists(data, "category", "title_fa")
        self.code:str = getIfExists(data, "category", "code")
        self.url:str = getIfExists(data, "category", "url", "uri")
        self.type:suggestionType = suggestionType.Normal

        if key == "categories":
            self.type = suggestionType.withCategory
        elif key == "auto_complete":
            self.type = suggestionType.Normal
        elif key == "advance_links":
            self.type = suggestionType.Advance
        elif key == "trends":
            self.type = suggestionType.Trend
            self.url = getIfExists(data, "url", "uri")


def parsSuggestions(data:dict) -> list[suggestionObj]:
    suggestions = []
    for key in data.keys():
        for item in data[key]:
            suggestions.append(suggestionObj(key, item))
    
    return suggestions