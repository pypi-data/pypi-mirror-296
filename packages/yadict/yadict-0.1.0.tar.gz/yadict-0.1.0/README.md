# yandex-dict
Module provides a client for the [Yandex Dictionary API](https://yandex.ru/dev/dictionary) of Yandex.Dictionary service.
The module contains class YandexDictionaryClient which is initialized with an API key from Yandex. It provides the following methods:

lookup(text, lang, ui=None, flags=None): Executes a search for a word or phrase in the Yandex Dictionary.
translate(text, lang): Translates a word in the specified language direction.
synonyms(text, lang): Finds the synonyms of a word in the specified language direction.
get_langs(): Makes a request to the Yandex Dictionary API to fetch a list of available translation directions.


See the [User Agreement of the Yandex API service.Dictionary](https://yandex.ru/legal/dictionary_api/) for more information about usage limits and conditions.
To get free API key use [page](https://yandex.ru/dev/dictionary/keys/get/?service=dict)

# Prerequisites
- Python 3.11 or later

# Installation
```bash
pip install yandex_dict
```

# Usage
```python
from yadict import YandexDictionaryClient

# Then create an instance of the client with your API key from Yandex:
client = YandexDictionaryClient("your-api-key")

# You can use the lookup method to search for a word or phrase in the dictionary:
result = client.lookup("time", "en-ru")
print(result)

# The translate method translates a word in the specified language direction:
translations = client.translate("time", "en-ru")
print(translations)  # ['время', 'час', 'эпоха', 'период времени', 'тайм', 'продолжительность', 'приурочивать', 'временной', 'своевременно']

# The synonyms method finds the synonyms of a word in the specified language direction:
synonyms = client.synonyms("time", "en-ru")
print(synonyms)  # ['время', 'минута', 'час', ...]

# The get_langs method fetches a list of available translation directions:
langs = client.get_langs()
print(langs)  # ['en-ru', 'ru-en', ...]
```
