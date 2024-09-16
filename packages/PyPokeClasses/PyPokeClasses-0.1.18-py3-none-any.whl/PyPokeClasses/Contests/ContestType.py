from __future__ import annotations
from ..Utility.Common import *

class ContestType(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/contest-type/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def berry_flavor(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"berry_flavor",NamedAPIResource)
    
    @property
    def names(self) -> Union[list[ContestName],None]:
        return Functions.convert_to_type_list(self._json_data,"names",ContestName)

class ContestName:
    def __init__(self,json_data):
        self.__json_data = json_data
        
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"name",str)
    
    @property
    def color(self) -> Union[str,None]:
        return Functions.convert_to_type(self.__json_data,"color",str)
    
    @property
    def language(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self.__json_data,"language",NamedAPIResource)
    