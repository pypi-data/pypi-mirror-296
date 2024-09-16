from ..Utility.Common import *

class Location(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/location/" + str(id))
        
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def region(self) -> Union[NamedAPIResource,None]:
        return Functions.convert_to_type(self._json_data,"region",NamedAPIResource)
  
    @property
    def names(self) -> Union[list[Name],None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)

    @property
    def game_indices(self) -> Union[list[GenerationGameIndex],None]:
        return Functions.convert_to_type_list(self._json_data,"game_indices",GenerationGameIndex)
    
    @property
    def areas(self) -> Union[list[NamedAPIResource],None]:
        return Functions.convert_to_type_list(self._json_data,"areas",NamedAPIResource)