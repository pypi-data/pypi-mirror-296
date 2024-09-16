from ..Utility.Common import *

class MoveCategory(BaseModel):
    def __init__(self,id):
        super().__init__("https://pokeapi.co/api/v2/move-category/" + str(id))
        
        
    @property
    def id(self) -> Union[int,None]:
        return Functions.convert_to_type(self._json_data,"id",int)
    
    @property
    def name(self) -> Union[str,None]:
        return Functions.convert_to_type(self._json_data,"name",str)
    
    @property
    def moves(self) -> Union[list[NamedAPIResource],None]:
        return Functions.convert_to_type_list(self._json_data,"moves",NamedAPIResource)
    
    @property
    def descriptions(self) -> Union[list[Description],None]:
        return Functions.convert_to_type_list(self._json_data,"descriptions",Description)