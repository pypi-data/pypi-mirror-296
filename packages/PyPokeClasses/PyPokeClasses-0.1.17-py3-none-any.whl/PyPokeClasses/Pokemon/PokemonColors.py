from ..Utility.Common import *

class PokemonColors(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/pokemon-color/" + str(id))
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def names(self) -> Union[list[Name],None]:
        return Functions.convert_to_type_list(self._json_data,"names",Name)
    
    @property
    def pokemon_species(self) -> Union[list[NamedAPIResource],None]:
        return Functions.convert_to_type_list(self._json_data,"pokemon_species",NamedAPIResource)