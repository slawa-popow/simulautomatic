
from abc import ABC, abstractmethod
from typing import Any, Union
from enum import Enum, auto

# ---------------------------------------------
class ThermoDeviceParameter(ABC):
    """Базовый для параметра терморегуляторов"""
    pass


# ---------------------------------------------
class DeviceDisplay(ABC):
    """Базовый для
    дисплеев приборов"""
    pass


# ---------------------------------------------
class DisplayBehavior(ABC):
    """Интерфейс для дисплеев."""

    @abstractmethod
    def float_print(self, value: float) -> None:
        pass

    @abstractmethod
    def int_print(self, value: int) -> None:
        pass

    @abstractmethod
    def str_print(self, value: str) -> None:
        pass

# ---------------------------------------------   
class SegmentDisplayBehavior(DisplayBehavior):
    """Интерфейс для дисплеев c 7
    сегментными индикаторами"""
    
    @abstractmethod
    def delimiter_point_print(self, position: int) -> None:
        pass


# ---------------------------------------------
# ---------------------------------------------
class SomeDisplay(SegmentDisplayBehavior):

    def __init__(self):
        pass

    def float_print(self, value):
        print(value)

    def int_print(self, value):
        print(value)

    def str_print(self, value):
        print(value)

    def delimiter_point_print(self, position):
        pass
# ---------------------------------------------
class SomeDisplayTwo(DisplayBehavior):
    def float_print(self, value):
        value = str(value)
        print(list(value))

    def int_print(self, value):
        print(list(str(value)))

    def str_print(self, value):
        print(list(value))
# ---------------------------------------------
# ---------------------------------------------
class ValueBehavior(ABC):
    """Интерфейс алгоритмов изменения
    значений параметров"""
    pass

# ---------------------------------------------
class DigitalBehavior:
    pass
# ---------------------------------------------
class IntBehavior(ValueBehavior, DigitalBehavior):
    
    def __init__(self, value) -> None:
        self.__value = value


# ---------------------------------------------
class FloatBehavior(ValueBehavior, DigitalBehavior):
    
    def __init__(self, value) -> None:
        self.__value = value


# ---------------------------------------------
class SelectBehavior(ValueBehavior):
    
    def __init__(self, value) -> None:
        self.__value = value


# ---------------------------------------------
class ViewBehavior(ABC):
    """Интерфейс поведения отображения
    значений параметров"""

    @abstractmethod
    def vprint(self, display: DisplayBehavior) -> None:
        pass


# ---------------------------------------------
class TypeValue(ABC):
    """Абстрактный базовый для реализаций"""

    def __init__(self, value_behavior: ValueBehavior, view_behavior: ViewBehavior) -> None:
        self.__value_behavior: ValueBehavior = value_behavior
        self.__view_behavior: ViewBehavior = view_behavior

    def print_value(self, display) -> str:
        return self.__view_behavior.vprint(display)
        

# ---------------------------------------------
class IntView(ViewBehavior):

    def __init__(self, value: int) -> None:
        self.__value: int = value
    
    def vprint(self, display: DisplayBehavior) -> None:
        display.int_print(f"IntView vprint {self.__value}")


# ---------------------------------------------
class FloatView(ViewBehavior):

    def __init__(self, value: float) -> None:
        self.__value: float = value

    def vprint(self, display: DisplayBehavior) -> None:
        display.float_print(f"FloatView vprint {self.__value}")


# ---------------------------------------------
class SelectView(ViewBehavior):

    def __init__(self, value: tuple) -> None:
        self.__value: tuple = value

    def vprint(self, display: DisplayBehavior) -> None:
        display.str_print(f"SelectView vprint {str.join('--', [str(s) for s in self.__value])}")

# ---------------------------------------------
class DigitalValue(TypeValue):
    """Реализация для int и float
    типов значений параметра"""

    def __init__(self, value_behavior, view_behavior) -> None:
        super().__init__(value_behavior, view_behavior)

# ---------------------------------------------
class SelectValue(TypeValue):
    """Реализация для выборочного
    типа значения параметров"""

    def __init__(self, value_behavior, view_behavior) -> None:
        super().__init__(value_behavior, view_behavior)


# ---------------------------------------------
class Value:
    """Фабрика типов."""
    
    class FactoryTypes(Enum):
        ENUM_INT = auto()
        ENUM_FLOAT = auto()
        ENUM_SELECT = auto()

    __factory_types: dict = {
        FactoryTypes.ENUM_INT: (DigitalValue, IntBehavior, IntView,),
        FactoryTypes.ENUM_FLOAT: (DigitalValue, FloatBehavior, FloatView,),
        FactoryTypes.ENUM_SELECT: (SelectValue, SelectBehavior, SelectView,),
    }

    @classmethod
    def __get_tuple_factory_types(cls, enum_type: FactoryTypes) -> tuple:
        return cls.__factory_types.get(enum_type)


    @classmethod
    def __get_type_value(cls, value: Union[int, float, tuple]) -> int:
        if isinstance(value, int):
            return cls.FactoryTypes.ENUM_INT
        elif isinstance(value, float):
            return cls.FactoryTypes.ENUM_FLOAT
        elif isinstance(value, tuple):
            return cls.FactoryTypes.ENUM_SELECT
        else:
            raise ValueError("__get_type_value() in Value => не корректный тип параметра <value>")
    

    def __init__(self, value: Union[int, float, tuple]) -> None:
        self.__value = value

    
    def __call__(self) -> TypeValue:
        type_value_enum = self.__get_type_value(self.__value)
        factory_types_tuple: tuple = self.__get_tuple_factory_types(type_value_enum)
        returned_instanse, value_behavior_type, view_behavior_type = factory_types_tuple
        
        return returned_instanse(value_behavior_type(self.__value), view_behavior_type(self.__value)) 

# ---------------------------------------------

# ---------------------------------------------

# ---------------------------------------------

class Parameter(ThermoDeviceParameter):
    """Параметр"""

    def __init__(self, name: str, value: Union[int, float, tuple]) -> None:
        self.__name: str = name
        self.__value: TypeValue = self.__get_instance_value(value)


    def __get_instance_value(self, value: Union[int, float, tuple]) -> TypeValue:
        __value = Value(value)
        return __value()

    @property
    def value(self) -> TypeValue:
        return self.__value


some_display = SomeDisplay()
some_display2 = SomeDisplayTwo()
al1 = Parameter("AL1", 140)
al2 = Parameter("AS", 0.25)
al1.value.print_value(some_display)
al2.value.print_value(some_display)
print("*"*45)
al1.value.print_value(some_display2)
al2.value.print_value(some_display2)