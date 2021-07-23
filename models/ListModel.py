from pydantic.generics import GenericModel
from typing import List, TypeVar, Generic

T = TypeVar('T')

class ListModel(GenericModel, Generic[T]):
    __root__: List[T]
    def __init__(self, *args, **kwargs):
        super().__init__(__root__=args, **kwargs)

    def __getitem__(self, key):
        return self.__root__[key]

    def __iter__(self):
        return iter(self.__root__)

    def __next__(self):
        return next(self.__root__)