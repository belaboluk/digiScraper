import sys
from pathlib import Path
import os
sys.path.append(str(Path(__file__).parents[1]))

from DigiScraper import digikala, suggestion, searchEngine

digi = digikala.DigiKala()

# searching in search bar and get suggestions back
suggestions = digi.getSuggestions("dvd")

for item in suggestions:
    if item.type == suggestion.suggestionType.withCategory:
        print(f"[Category] {item.keyword} in {item.category} category [{item.code}]")
    elif item.type == suggestion.suggestionType.Normal:
        print(f"[Normal]   {item.keyword}")
    elif item.type == suggestion.suggestionType.Advance:
        print(f"[Advance]  {item.keyword} with url {item.url}")
    elif item.type == suggestion.suggestionType.Trend:
        print(f"[trend]    {item.keyword} with url {item.url}")


# getting search result of one of the abouve suggestions
result = digi.search(suggestions[0])
print(len(result.products))

# creating a sort option 
# when creating a sort option manualy the sort option can be unvalid if the sort id is not validby digikala so it's suggested to seleect a sortoption from a lasr search instead of creating one manualy
digiKalaSort = searchEngine.createSortOption(4)
result = digi.search(suggestions[3], 2, digiKalaSort)
print(len(result.products))

# selecting a sort option from last search result
digiKalaSort = None
for i in result.sortOptions:
    if i.text == "گران‌ترین":
        digiKalaSort = i
result = digi.search(suggestions[8], sortOptions=digiKalaSort)
print(len(result.products))

# creating a filter for search
# be carefull the manul filter creation can be a unvalid filter from that product
# so it's suggested to search filsr then get all the filters thst availabel for that product the select that filter and serch again with that filter 
digiKalaFilters = []
digiKalaFilters.append(searchEngine.createFilter("trusted", searchEngine.FilterType.Checkbox, "seller_types"))
digiKalaFilters.append(searchEngine.createPriceRangeFilter(0, 500000))
# selecting a filter option from last search result
digiKalaFilters.append(result.findFilterOptionByName("فقط در شهر تهران"))
# digiKalaFilters.append(result.findFilterOptionByName("ال جی"))
# digiKalaFilters.append(result.findFilterOptionByID(93))

result = digi.search(suggestions[8], sortOptions = result.selectSortOption(7), filterOptions = digiKalaFilters)
print(len(result.products))

# getting search result of manual search (without any digikala suggestion)
result = digi.search("کیف", 2)
print(len(result.products))

