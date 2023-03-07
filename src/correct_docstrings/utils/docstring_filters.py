"""
Collection of filters for a single docstring.
"""
import string
from abc import ABC
from typing import Tuple, List


class DocstringFilterBase(ABC):
    """
    Base class for docstring filters.
    """

    def format(self, content: Tuple[str]) -> Tuple[str]:
        """
        Formats the content.

        :param content: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """
        pass


class EmptyLineBetweenDescriptionAndParams(DocstringFilterBase):
    """
    Docstring filter that makes sure that there is an empty line between description and params.

    :param prefixes: list of prefixes that indicate a docstring keyword.

    Example:
        Description of the function.
        :param _: some description
        :return: some description

    will be changed to:
        Description of the function.

        :param _: some description
        :return: some description
    """

    def __init__(self, prefixes: Tuple[str] = (":param", ":return", ":raises")):
        """
        :param prefixes: list of prefixes that indicate the start of the param list.
        """
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that there is an empty line between description and params.

        :param docstring: list of lines in docstring
        :return: list of lines in docstring
        """
        start_of_param_list = -1
        docstring = docstring.copy()

        for i, line in enumerate(docstring):
            line = line.strip()
            # check if it starts with prefix
            for prefix in self.prefixes:
                if line.startswith(prefix) and i > 1:
                    start_of_param_list = i
                    break

            if start_of_param_list != -1:
                break

        if start_of_param_list == -1:
            return docstring

        # remove all empty lines before param list and enter a single empty line
        # before param list
        while docstring[start_of_param_list - 1].strip() == "":
            docstring.pop(start_of_param_list - 1)
            start_of_param_list -= 1

        docstring.insert(start_of_param_list, "")

        return docstring


class RemoveUnwantedPrefixes(DocstringFilterBase):
    """
    Docstring filter that removes unwanted prefixes from the docstring.

    :param prefixes: list of prefixes that indicate a docstring keyword.

    Example:
     .. :param _: some description
        ,:return: some description

    will be changed to:
        :param _: some description
        :return: some description
    """

    def __init__(self, prefixes: Tuple[str] = (":param", ":return", ":raises")):
        """
        :param prefixes: list of prefixes that indicate the start of the param list.
        """
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Removes unwanted prefixes from the docstring.

        :param docstring: list of lines in docstring
        :return: list of lines in docstring
        """
        for i, line in enumerate(docstring):
            # check if one prefixes is in line
            for prefix in self.prefixes:
                index = line.find(prefix)
                if index != -1:
                    # make sure there is only whitespace before prefix
                    # replace all characters before prefix with whitespace
                    docstring[i] = " " * index + line[index:]
                    break

        return docstring


class NoRepeatedWhitespaces(DocstringFilterBase):
    """
    Docstring filter that removes repeated whitespaces from the docstring.

    :param prefixes: list of prefixes that indicate a docstring keyword.

    Example:
        :param _:     some description
        :return: some description

    will be changed to:
        :param _: some description
        :return: some description
    """

    def __init__(self, prefixes: Tuple[str] = (":param", ":return", ":raises")):
        """
        :param prefixes: list of prefixes that indicate the start of the param list.
        """
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Removes repeated whitespaces from the docstring.

        :param docstring: list of lines in docstring
        :return: list of lines in docstring
        """
        for i, line in enumerate(docstring):
            for prefix in self.prefixes:
                index = line.find(prefix)
                if index != -1:
                    index_of_second_semicolon = line.find(":", index + len(prefix))
                    if index_of_second_semicolon != -1:
                        line_after_second_semicolon = line[
                            index_of_second_semicolon + 1 :
                        ]

                        while line_after_second_semicolon.startswith(" "):
                            line_after_second_semicolon = line_after_second_semicolon[
                                1:
                            ]

                        if len(line_after_second_semicolon) > 1:
                            line_after_second_semicolon = (
                                " "
                                + line_after_second_semicolon[0]
                                + line_after_second_semicolon[1:]
                            )

                        docstring[i] = (
                            line[: index_of_second_semicolon + 1]
                            + line_after_second_semicolon
                        )

        return docstring


class EndOfSentencePunctuation(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each sentence ends
    with a punctuation mark.

    :param punctuation: punctuation mark to be used.

    Example:
        :param _: some description
        :return: some description

    will be changed to:
        :param _: some description.
        :return: some description.
    """

    def __init__(self, punctuation: str = "."):
        self.punctuation = punctuation

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each sentence ends with a punctuation mark. If a sentence
        spans multiple lines, the last line of the sentence is the one that ends
        with a punctuation mark.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            line = line.strip()
            if not line:
                continue

            if line.endswith(self.punctuation):
                continue

            if not any(char.isalpha() for char in line):
                continue

            if line[-1] in string.punctuation:
                continue

            if i + 1 >= len(docstring):
                docstring[i] = docstring[i].rstrip() + self.punctuation
                continue

            j = i + 1
            next_line = docstring[j].strip()

            while not next_line and j < len(docstring):
                next_line = docstring[j].strip()
                j += 1

            if next_line.startswith(":") or j + 1 >= len(docstring):
                docstring[i] = docstring[i].rstrip() + self.punctuation

        return docstring


class EnsureColonInParamDescription(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each parameter description
    starts with ':param <param_name>:'.

    Example:
        :param _ some description
        :return: some description

    will be changed to:
        :param _: some description
        :return: some description
    """

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each parameter description starts with ':param <param_name>:'.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            if not line:
                continue

            if line.strip().startswith(":param") and (
                line.count(":") == 1 or len(line.strip().split(":")[1].split(" ")) != 2
            ):
                j = line.index(":")
                # find the second word in the line after j and add a colon after it
                j += line[j + 1 :].index(" ") + 1
                j += line[j + 1 :].index(" ") + 1
                docstring[i] = line[:j] + line[j:].replace(" ", ": ", 1)

            while "::" in docstring[i]:
                docstring[i] = docstring[i].replace("::", ":")

        return docstring


class IndentMultilineParamDescription(DocstringFilterBase):
    """
    Docstring filter that is responsible for indenting multiline parameter descriptions.

    :param indentation: indentation to be used.

    Example:
        :param _: some description
        that spans multiple lines
        :return: some description

    will be changed to:
        :param _: some description
          that spans multiple lines
        :return: some description
    """

    def __init__(self, indentation: str = " " * 2):
        self.indentation = indentation

    def format(self, docstring: List[str]) -> List[str]:
        """
        Indents multiline parameter descriptions.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            if not line:
                continue

            next_line = docstring[i + 1] if i + 1 < len(docstring) else None
            if not next_line:
                continue

            j = 0
            while line.strip().startswith(
                ":param"
            ) and not next_line.strip().startswith(":"):
                j += 1
                next_line = docstring[i + j] if i + j < len(docstring) else None

                if not next_line or next_line.strip().startswith(":"):
                    j -= 1
                    break

            default_indentation = " " * (len(line) - len(line.lstrip()))
            for k in range(j):
                index = i + k + 1
                if index >= len(docstring):
                    break
                docstring[index] = (
                    default_indentation + self.indentation + docstring[index].lstrip()
                )

        return docstring


class SentenceCapitalization(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each sentence starts
    with a capital letter.

    :param prefixes: prefixes of the lines that should be ignored.

    Example:
        :param _: some description
        :return: some description

    will be changed to:
        :param _: Some description
        :return: Some description
    """

    def __init__(self, prefixes: Tuple[str] = (":param", ":return", ":raises")):
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each sentence starts with a capital letter. If a sentence
        spans multiple lines, the first line of the sentence is the one that starts
        with a capital letter.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            for prefix in self.prefixes:
                index = line.find(prefix)
                if index != -1:
                    index_of_second_semicolon = line.find(":", index + len(prefix))
                    if index_of_second_semicolon != -1:
                        line_after_second_semicolon = line[
                            index_of_second_semicolon + 1 :
                        ]

                        while line_after_second_semicolon.startswith(" "):
                            line_after_second_semicolon = line_after_second_semicolon[
                                1:
                            ]

                        if len(line_after_second_semicolon) > 1:
                            line_after_second_semicolon = (
                                " "
                                + line_after_second_semicolon[0].upper()
                                + line_after_second_semicolon[1:]
                            )

                        docstring[i] = (
                            line[: index_of_second_semicolon + 1]
                            + line_after_second_semicolon
                        )

        return docstring


class LineWrapping(DocstringFilterBase):
    """
    Docstring filter that is responsible for wrapping lines at a given maximum length.

    :param max_length: maximum length of each line.
    :param prefixes: prefixes of the lines that should be ignored.
    """

    def __init__(
        self, max_length: int, prefixes: Tuple[str] = (":param", ":return", ":raises")
    ):
        self.max_length = max_length
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Wraps lines at a given maximum length.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """
        result = []
        for i, line in enumerate(docstring):
            result.append(line)
            for prefix in self.prefixes:
                index = line.find(prefix)
                if index != -1:
                    index_of_second_semicolon = line.find(":", index + len(prefix))
                    if index_of_second_semicolon != -1:
                        line_after_second_semicolon = line[
                            index_of_second_semicolon + 1 :
                        ]

                        while line_after_second_semicolon.startswith(" "):
                            line_after_second_semicolon = line_after_second_semicolon[
                                1:
                            ]

                        if len(line_after_second_semicolon) > self.max_length:
                            last_space_index = line_after_second_semicolon.rfind(
                                " ", 0, self.max_length
                            )
                            if last_space_index != -1:
                                result = result[:-1]
                                result.append(
                                    line_after_second_semicolon[:last_space_index]
                                )
                                result.append(
                                    line_after_second_semicolon[last_space_index + 1 :]
                                )

        return docstring


class ThirdPersonConverter(DocstringFilterBase):
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
                word, punctuation = ThirdPersonConverter.split_punctuation(word)
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


class DocstringFormatter:
    """
    Gathers the docstring filters and applies them to the docstring
    when the format method is called.

    :param docstring_filters: list of docstring filters.
    """

    def __init__(self, docstring_filters: Tuple[DocstringFilterBase]):
        self.filters = docstring_filters

    def format(self, docstring: List[str]) -> List[str]:
        """
        Formats the docstring using the specified filters.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for docstring_filter in self.filters:
            docstring = docstring_filter.format(docstring)

        return docstring
