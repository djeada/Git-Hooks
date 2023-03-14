import re

from src.docstring_physician.filters.docstrings_validators.validator_base import (
    ValidatorBase,
)
from src.docstring_physician.parsers.param_parser.param_parser import (
    ParametersExtractor,
)


class PublicFunctionParameterPresenceValidator(ValidatorBase):
    """
    A filter that checks if all parameters in public function docstrings match
    the function signatures.
    """

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
                original_i = i + 1

                func_name = line.split()[1].split("(")[0]
                if func_name.startswith("_") or (
                    i - 1 >= 0 and re.findall(r"@\w+\.(setter|deleter)", content[i - 1])
                ):
                    continue
                # Function is public
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                extractor = ParametersExtractor(content)
                function_parameters = extractor.extract_parameters(i, end_index)

                next_line = end_index + 1
                if next_line < len(content) and content[next_line].strip().startswith(
                    '"""'
                ):
                    docstring_content = []
                    description_started = False
                    for j in range(next_line, len(content)):
                        docstring_line = content[j].strip()
                        if not description_started and docstring_line.startswith('"""'):
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
                            print(
                                f"{original_i}: Parameter mismatch in function {func_name}"
                            )
                        return False
        return True
