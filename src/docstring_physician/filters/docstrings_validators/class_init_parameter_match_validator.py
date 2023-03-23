import re
from typing import List

from src.docstring_physician.filters.docstrings_validators.validator_base import (
    DocstringValidatorBase,
)
from src.docstring_physician.parsers.param_parser.param_parser import (
    ParametersExtractor,
)


class ClassInitParameterMatchValidator(DocstringValidatorBase):
    def check(self, content: List[str], verbosity: bool = True) -> bool:
        """
        Checks if all classes in the content parameter have docstrings with
        descriptions for all of their __init__ method parameters.

        :param content: List of lines in the Python script.
        :param verbosity: If True, displays a message before returning False.
        :return: True if all classes have parameter descriptions, else False.
        """

        i = 0
        while i < len(content):
            line = content[i].strip()
            if line.startswith("class"):
                class_name = line.split()[1].split("(")[0]
                class_docstring_start = -1
                init_start = -1

                # Increment i to avoid infinite loop
                i += 1

                # Find class docstring and __init__ method
                while i < len(content):
                    line = content[i].strip()

                    if line.startswith('"""') and class_docstring_start == -1:
                        class_docstring_start = i

                    if line.startswith("def __init__"):
                        init_start = i
                        break

                    if line.startswith("class"):
                        break

                    i += 1

                # Check if __init__ method exists
                if init_start == -1:
                    continue

                # Find the end index of the __init__ method
                init_end = i
                while init_end < len(content) and not content[
                    init_end
                ].strip().startswith("def"):
                    init_end += 1

                # Extract __init__ method parameters
                extractor = ParametersExtractor(content)
                init_parameters = extractor.extract_parameters(init_start, init_end)

                # Find class docstring content
                if class_docstring_start != -1:
                    class_docstring_content = []
                    description_started = False
                    for j in range(class_docstring_start, len(content)):
                        docstring_line = content[j].strip()
                        if not description_started and docstring_line.startswith('"""'):
                            description_started = True
                        elif description_started and docstring_line.endswith('"""'):
                            break
                        elif description_started:
                            class_docstring_content.append(docstring_line)

                    class_docstring = " ".join(class_docstring_content).strip()
                    class_docstring_parameters = re.findall(
                        r":param ([^:]+):", class_docstring
                    )
                    # Debug info
                    print(
                        "Init parameters: ",
                        [parameter.name for parameter in init_parameters],
                    )
                    print("Class docstring parameters: ", class_docstring_parameters)
                    if not set(
                        [parameter.name for parameter in init_parameters]
                    ).issubset(set(class_docstring_parameters)):
                        if verbosity:
                            print(
                                f"{class_docstring_start}: Class {class_name} is missing __init__ parameter descriptions in its docstring."
                            )
                        # Parameter mismatch between class docstring and __init__ method signature
                        return False

            i += 1

        return True
