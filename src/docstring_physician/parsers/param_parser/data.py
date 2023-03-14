from dataclasses import dataclass


@dataclass
class ParameterData:
    """
    Holds information about a parameter.

    :param name: name of the parameter
    :param type_hint: type hint of the parameter
    :param default_value: default value of the parameter
    :param description: description of the parameter
    """

    name: str
    type_hint: str
    default_value: str = ""
    description: str = ""

    def __str__(self):
        return (
            f"{self.name}: {self.type_hint} = {self.default_value}"
            if self.default_value
            else f"{self.name}: {self.type_hint}"
        )
