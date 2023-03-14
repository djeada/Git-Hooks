from typing import List, Tuple


class DocstringsLocalizer:
    """
    Finds docstrings in a python file.

    :param content: python file content as a list of lines
    """

    def __init__(self, content: List[str]):
        self.content = content

    def find_next_docstring(self, index: int) -> Tuple[int, int]:
        """
        Finds next docstring in content starting from index. Returns (-1, -1) if no docstring found.

        :param index: index to start looking for docstring
        :return: start and end position of docstring
        """
        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]
        corresponding_docstring_end = {
            '"""': '"""',
            "'''": "'''",
            'r"""': '"""',
            "r'''": "'''",
        }

        for i in range(index, len(self.content)):
            line = self.content[i].strip()
            if line in possible_docstring_start:
                for j in range(i + 1, len(self.content)):
                    next_line = self.content[j].strip()
                    if next_line == corresponding_docstring_end[line]:
                        return i, j

        return -1, -1

    def find_all_docstrings(self) -> List[Tuple[int, int]]:
        """
        Finds all docstrings in content. Returns empty list if no docstring found.

        :return: list of start and end position of docstrings
        """
        docstrings = []
        next_docstring_pos = self.find_next_docstring(0)
        while next_docstring_pos != (-1, -1):
            docstrings.append(next_docstring_pos)
            next_docstring_pos = self.find_next_docstring(next_docstring_pos[1] + 1)

        return docstrings
