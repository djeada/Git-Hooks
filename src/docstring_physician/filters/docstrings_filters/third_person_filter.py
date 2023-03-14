from typing import Tuple, List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class ThirdPersonFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that every verb in the docstring
    is in the third person.

    :param blocking_words: if a verb is preceded by one of these words, it will not be changed.
    :param modals: list of modal verbs that should not be changed.
    :param verbs: list of words that should be changed to the third person.


    Example:
        Calculate the sum of two numbers.

    will be changed to:
        Calculates the sum of two numbers.
    """

    def __init__(
        self, blocking_words: Tuple[str], modals: Tuple[str], verbs: Tuple[str]
    ):
        self.blocking_words = blocking_words
        self.modals = modals
        self.verbs = verbs

    def format(self, docstring: List[str]) -> List[str]:
        """
        Converts the verbs in the docstring to third-person singular form.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """
        # check which line starts with ":"
        end_index = -1
        for i, line in enumerate(docstring):
            line = line.strip()
            if line.startswith(":"):
                end_index = i
                break

        if end_index == -1:
            return docstring

        for i in range(1, end_index):
            line = docstring[i]
            leading_whitespaces = len(line) - len(line.lstrip())
            new_line = " " * leading_whitespaces
            previous_word = ""
            for word in line.split():
                word, punctuation = ThirdPersonFilter.split_punctuation(word)
                if (
                    previous_word.lower() not in self.blocking_words
                    and previous_word.lower() not in self.verbs
                    and not previous_word.lower().endswith("n't")
                ):
                    word = self.convert_to_third_person_singular(word)
                new_line += word + punctuation + " "
                previous_word = word

            docstring[i] = new_line.rstrip()

        return docstring

    def convert_to_third_person_singular(self, word: str) -> str:
        """
        Convert word to third-person singular form.

        :param word: word to convert.
        :return: third-person singular form of word.
        """
        if not self.is_verb(word):
            return word
        if word.lower() in self.modals:
            return word

        # Add –es instead of –s if the base form ends in -s, -z, -x, -sh, -ch, or the vowel o (but not -oo).

        if (
            word.lower()[-1]
            in [
                "s",
                "z",
                "x",
                "sh",
                "ch",
                "o",
            ]
            and not word.lower().endswith("oo")
        ):
            return word + "es"

        # If the base form ends in consonant + y, remove the -y and add –ies.
        if word.lower()[-1] == "y":
            return word[:-1] + "ies"

        return word + "s"

    def is_verb(self, word: str) -> bool:
        """
        Check if word is a verb

        :param word: word to check
        :return: True if word is a verb, False otherwise
        """
        return word.lower().strip() in self.verbs

    @staticmethod
    def split_punctuation(word: str) -> Tuple[str, str]:
        """
        Splits the word into two parts: word and punctuation.

        :param word: word to split
        :return: word and punctuation
        """
        letters = ""

        end_index = -1
        for i, letter in enumerate(word):
            if not letter.isalpha():
                end_index = i
                break
            letters += letter

        punctuation = word[end_index:] if end_index != -1 else ""

        return letters, punctuation
