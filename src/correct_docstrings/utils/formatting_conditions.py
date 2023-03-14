import re
from abc import ABC
from typing import Tuple, Type

from src.correct_docstrings.utils.helpers import ParametersExtractor


class FormattingConditionFilterBase(ABC):
    """
    Base class for formatting condition filters.
    """

    def check(self, content: Tuple[str]) -> bool:
        """
        Checks the content.

        :param content: list of content in the docstring.
        :return: True if everything is fine, else otherwise.
        """
        pass


class ModuleDocstringFilter(FormattingConditionFilterBase):
    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
        """
        Checks if the first non-empty line of the content parameter
        is a module docstring that starts with either \"\"\" or '''.

        :param content: Text of Python script.
        :param verbosity: Whether or not to display a message before returning False.
        :return: True if module docstring is present, else False.
        """
        for line in content:
            if line.strip() != "":
                if line.startswith('"""') or line.startswith("'''"):
                    return True
                else:
                    if verbosity:
                        print("Module docstring is missing or improperly formatted.")
                    return False
        if verbosity:
            print("Module docstring is missing.")
        return False


class PublicClassDocstringFilter(FormattingConditionFilterBase):
    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
        """
        Checks if all public classes in the content parameter have docstrings
        immediately below their definition.

        :param content: Text of Python script.
        :param verbosity: Whether or not to display a message before returning False.
        :return: True if all public classes have docstrings, else False.
        """
        for line in content:
            if line.strip().startswith("class"):
                class_name = line.split()[1]
                if not class_name.startswith("_"):
                    # Class is public
                    next_line = content.index(line) + 1
                    if next_line < len(content) and content[
                        next_line
                    ].strip().startswith('"""'):
                        # Public class has a docstring
                        continue
                    else:
                        # Public class is missing docstring
                        if verbosity:
                            print(
                                f"The public class {class_name} is missing a docstring."
                            )
                        return False
        return True


class PublicFunctionDocstringFilter(FormattingConditionFilterBase):
    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
        """
        Checks if all public functions in the content parameter have docstrings
        immediately below their definition.

        :param content: Text of Python script.
        :param verbosity: Whether to display appropriate message before returning False (default=True).
        :return: True if all public functions have docstrings, else False.
        """
        for line in content:
            if line.strip().startswith("def"):
                func_name = line.split()[1].split("(")[0]
                if not func_name.startswith("_"):
                    # Function is public
                    next_line = content.index(line) + 1
                    if next_line < len(content) and content[
                        next_line
                    ].strip().startswith('"""'):
                        # Public function has a docstring
                        continue
                    else:
                        # Public function is missing docstring
                        if verbosity:
                            print(f"Function {func_name} is missing a docstring.")
                        return False
        return True


class PublicFunctionParameterDocstringFilter(FormattingConditionFilterBase):
    def check(self, content: str, verbosity: bool = True) -> bool:
        """
        Checks if all public functions in the content parameter have docstrings
        with descriptions for all of their parameters.

        :param content: Text of Python script.
        :param verbosity: If True, displays a message before returning False.
        :return: True if all public functions have parameter descriptions, else False.
        """
        for i in range(len(content) - 1):
            line = content[i].strip()
            if line.startswith("def"):
                func_name = line.split()[1].split("(")[0]
                if not func_name.startswith("_"):
                    # Function is public
                    end_index = i
                    while not line.endswith(":"):
                        end_index += 1
                        line = content[end_index].strip()

                    extractor = ParametersExtractor(content)
                    function_parameters = extractor.extract_parameters(i, end_index)

                    next_line = end_index + 1
                    if next_line < len(content) and content[
                        next_line
                    ].strip().startswith('"""'):
                        docstring_content = []
                        description_started = False
                        for j in range(next_line, len(content)):
                            docstring_line = content[j].strip()
                            if not description_started and docstring_line.startswith(
                                '"""'
                            ):
                                description_started = True
                            elif description_started and docstring_line.endswith('"""'):
                                break
                            elif description_started:
                                docstring_content.append(docstring_line)

                        docstring = " ".join(docstring_content).strip()
                        docstring_parameters = re.findall(r":param ([^:]+):", docstring)
                        if not set(
                            [parameter.name for parameter in function_parameters]
                        ).issubset(set(docstring_parameters)):
                            if verbosity:
                                print(
                                    f"Function {func_name} is missing parameter descriptions in its docstring."
                                )
                            # Parameter mismatch between docstring and function signature
                            return False
        return True


class PublicFunctionParameterMismatchFilter(FormattingConditionFilterBase):
    def check(self, content: str, verbosity: bool = True) -> bool:
        """
        Checks if all parameters in public function docstrings match the
        function signatures.

        :param content: Text of Python script.
        :param verbosity: Whether to display appropriate messages before returning False (default: True).
        :return: True if all public function parameters match their docstring
        descriptions, else False.
        """
        func_name = None
        for i in range(len(content) - 1):
            line = content[i].strip()
            if line.startswith("def"):
                func_name = line.split()[1].split("(")[0]
                if not func_name.startswith("_"):
                    # Function is public
                    end_index = i
                    while not line.endswith(":"):
                        end_index += 1
                        line = content[end_index].strip()

                    extractor = ParametersExtractor(content)
                    function_parameters = extractor.extract_parameters(i, end_index)

                    next_line = end_index + 1
                    if next_line < len(content) and content[
                        next_line
                    ].strip().startswith('"""'):
                        docstring_content = []
                        description_started = False
                        for j in range(next_line, len(content)):
                            docstring_line = content[j].strip()
                            if not description_started and docstring_line.startswith(
                                '"""'
                            ):
                                description_started = True
                            elif description_started and docstring_line.endswith('"""'):
                                break
                            elif description_started:
                                docstring_content.append(docstring_line)

                        docstring = " ".join(docstring_content).strip()
                        docstring_parameters = re.findall(r":param ([^:]+):", docstring)
                        if not set(docstring_parameters).issubset(
                            set([parameter.name for parameter in function_parameters])
                        ):
                            # Parameter mismatch between docstring and function signature
                            if verbosity:
                                print(f"Parameter mismatch in function {func_name}")
                            return False
        return True


class FormattingConditionValidator:
    """
    Gathers the formatting condition filters and applies them to the content
    when the check method is called.

    :param filters: list of formatting condition filters.
    """

    def __init__(self, filters: Tuple[Type[FormattingConditionFilterBase]]):
        self.filters = filters

    def check(self, content: Tuple[str]) -> bool:
        """
        Applies the formatting condition filters to the content and returns True
        if everything passes, else False.

        :param content: list of content in the content.
        :return: True if everything passes, else False.
        """

        for filter_class in self.filters:
            filter_instance = filter_class()
            if isinstance(filter_instance, FormattingConditionFilterBase):
                if not filter_instance.check(content):
                    return False

        return True
