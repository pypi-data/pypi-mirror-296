"""all Type Enums and related helpers in card message"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, Dict, List


class _TypeEnum(Enum):
    """base class of all types(involved in card components)

    remind: TypeEnum implements _repr but not inherits from Representable,
    since "TypeError: metaclass conflict:
    the metaclass of a derived class must be a (non-strict) subclass of the
    metaclasses of all its bases"
    """

    @property
    def _repr(self):
        return self.value


class Types:
    """contains all types used in card messages"""

    class Theme(_TypeEnum):
        """describes a component's theme, controls its color"""
        NA = ''
        PRIMARY = 'primary'
        SECONDARY = 'secondary'
        SUCCESS = 'success'
        DANGER = 'danger'
        WARNING = 'warning'
        INFO = 'info'
        NONE = 'none'

    class Size(_TypeEnum):
        """describes a component's size"""
        NA = ''
        XS = 'xs'
        SM = 'sm'
        MD = 'md'
        LG = 'lg'

    class Text(_TypeEnum):
        """which type of text"""
        PLAIN = 'plain-text'
        MD = 'kmarkdown'

    class Click(_TypeEnum):
        """used in button, determines the behavior of button when clicked"""
        LINK = 'link'
        RETURN_VAL = 'return-val'

    class SectionMode(_TypeEnum):
        """used in section, arrangement of elements in"""
        LEFT = 'left'
        RIGHT = 'right'

    class File(_TypeEnum):
        """which type of file"""
        FILE = 'file'
        AUDIO = 'audio'
        VIDEO = 'video'

    class CountdownMode(_TypeEnum):
        """used in countdown module, determines its layout"""
        DAY = 'day'
        HOUR = 'hour'
        SECOND = 'second'
