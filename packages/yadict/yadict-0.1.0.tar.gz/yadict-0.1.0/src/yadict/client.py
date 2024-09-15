"""
Module provides a client for the [Yandex Dictionary API](https://yandex.ru/dev/dictionary) of Yandex.Dictionary service.
The module contains class YandexDictionaryClient which is initialized with an API key from Yandex. It provides the following methods:

lookup(text, lang, ui=None, flags=None): Executes a search for a word or phrase in the Yandex Dictionary.
translate(text, lang): Translates a word in the specified language direction.
synonyms(text, lang): Finds the synonyms of a word in the specified language direction.
get_langs(): Makes a request to the Yandex Dictionary API to fetch a list of available translation directions.


See the [User Agreement of the Yandex API service.Dictionary](https://yandex.ru/legal/dictionary_api/) for more information about usage limits and conditions.
To get free API key use [page](https://yandex.ru/dev/dictionary/keys/get/?service=dict)
"""

import requests
from typing import List, Optional


class YandexDictionaryClient:
    BASE_URL_LOOKUP = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
    BASE_URL_GETLANGS = "https://dictionary.yandex.net/api/v1/dicservice.json/getLangs"

    def __init__(self, api_key):
        self.api_key = api_key

    def lookup(self, text, lang, ui=None, flags=None):
        """
        Executes a search for a word or phrase in the Yandex Dictionary.

        Args:
            text (str): The word or phrase to be searched.
            lang (str): Translation direction e.g "en-ru".
            ui (str, optional): User interface language.
            flags (int, optional): Search options as a bit mask of flags.

        Returns:
            dict: Response from the Yandex Dictionary API in JSON format.

        Raises:
            requests.RequestException: If an error occurred during the request execution.
        """
        params = {"key": self.api_key, "lang": lang, "text": text}

        if ui:
            params["ui"] = ui
        if flags is not None:
            params["flags"] = flags

        try:
            response = requests.get(self.BASE_URL_LOOKUP, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Error occurred during the request execution: {e}"
            )

    def translate(self, text, lang):
        """
        Translates a word in the specified language direction.

        Args:
            text (str): The word to be translated.
            lang (str): Translation direction e.g "en-ru".

        Returns:
            list of str: A list of possible translations for the word.

        Raises:
            requests.RequestException: If an error occurred during the request execution.
        """
        response = self.lookup(text, lang, flags=self.Flags.MORPHO)
        translations = []

        for entry in response.get("def", []):
            for tr in entry.get("tr", []):
                translations.append(tr["text"])

        return translations

    def synonyms(self, text, lang):
        """
        Finds the synonyms of a word in the specified language direction.

        Args:
            text (str): The word to find synonyms for.
            lang (str): Translation direction e.g "en-ru".

        Returns:
            list of str: A list of possible synonyms for the word.

        Raises:
            requests.RequestException: If an error occurred during the request execution.
        """
        response = self.lookup(text, lang)
        synonyms = []

        for entry in response.get("def", []):
            for trans in entry.get("tr", []):
                for syn in trans.get("syn", []):
                    synonyms.append(syn["text"])

        return synonyms

    def get_langs(self):
        """
        Makes a request to the Yandex Dictionary API to fetch a list of available translation directions.

        Returns:
            list of str: A list of possible translation directions.

        Raises:
            requests.RequestException: If an error occurred during the request execution.
        """
        response = requests.get(
            f"{self.BASE_URL_GETLANGS}", params={"key": self.api_key}
        )
        response.raise_for_status()

        return response.json()

    @staticmethod
    class Flags:
        FAMILY = 0x0001
        SHORT_POS = 0x0002
        MORPHO = 0x0004
        POS_FILTER = 0x0008


def lookup(
    api_key: str,
    text: str,
    lang: str,
    ui: Optional[str] = None,
    flags: Optional[int] = None,
) -> dict:
    """
    Executes a search for a word or phrase in the Yandex Dictionary.

    Args:
        api_key (str): The API key from Yandex.
        text (str): The word or phrase to be searched.
        lang (str): Translation direction e.g "en-ru".
        ui (str, optional): User interface language.
        flags (int, optional): Search options as a bit mask of flags.

    Returns:
        dict: Response from the Yandex Dictionary API in JSON format.

    Raises:
        requests.RequestException: If an error occurred during the request execution.
    """
    params = {"key": api_key, "lang": lang, "text": text}

    if ui:
        params["ui"] = ui
    if flags is not None:
        params["flags"] = flags

    try:
        response = requests.get(
            "https://dictionary.yandex.net/api/v1/dicservice.json/lookup", params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(
            f"Error occurred during the request execution: {e}"
        )


def translate(api_key: str, text: str, lang: str) -> List[str]:
    """
    Translates a word in the specified language direction.

    Args:
        api_key (str): The API key from Yandex.
        text (str): The word to be translated.
        lang (str): Translation direction e.g "en-ru".

    Returns:
        list of str: A list of possible translations for the word.

    Raises:
        requests.RequestException: If an error occurred during the request execution.
    """
    response = lookup(api_key, text, lang, flags=Flags.MORPHO)
    translations = []

    for entry in response.get("def", []):
        for tr in entry.get("tr", []):
            translations.append(tr["text"])

    return translations


def synonyms(api_key: str, text: str, lang: str) -> List[str]:
    """
    Finds the synonyms of a word in the specified language direction.

    Args:
        api_key (str): The API key from Yandex.
        text (str): The word to find synonyms for.
        lang (str): Translation direction e.g "en-ru".

    Returns:
        list of str: A list of possible synonyms for the word.

    Raises:
        requests.RequestException: If an error occurred during the request execution.
    """
    response = lookup(api_key, text, lang)
    synonyms = []

    for entry in response.get("def", []):
        for trans in entry.get("tr", []):
            for syn in trans.get("syn", []):
                synonyms.append(syn["text"])

    return synonyms


def get_langs(api_key: str) -> List[str]:
    """
    Makes a request to the Yandex Dictionary API to fetch a list of available translation directions.

    Args:
        api_key (str): The API key from Yandex.

    Returns:
        list of str: A list of possible translation directions.

    Raises:
        requests.RequestException: If an error occurred during the request execution.
    """
    response = requests.get(
        "https://dictionary.yandex.net/api/v1/dicservice.json/getLangs",
        params={"key": api_key},
    )
    response.raise_for_status()

    return response.json()


class Flags:
    FAMILY = 0x0001
    SHORT_POS = 0x0002
    MORPHO = 0x0004
    POS_FILTER = 0x0008
