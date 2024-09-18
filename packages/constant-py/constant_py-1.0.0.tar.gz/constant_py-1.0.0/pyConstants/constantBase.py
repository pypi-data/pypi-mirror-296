import os


class ConstantClass:
    def __setattr__(self, name, value) -> None:
        if name in self.__dict__:
            raise AttributeError(f"Cannot reassign constant {name}")
        self.__dict__[name] = value

class Constant:
    @staticmethod
    def __constantError__() -> None:
        raise AttributeError("Cannot reassign constant")

    @staticmethod
    def Constant(value) -> property:
        Property = property(fget=lambda: value, fset=Constant.__constantError__)
        return Property
    
    @staticmethod
    def ConstantProperty(setFunc: function) -> property:
        Property = property(fget=setFunc, fset=Constant.__constantError__)
        return Property