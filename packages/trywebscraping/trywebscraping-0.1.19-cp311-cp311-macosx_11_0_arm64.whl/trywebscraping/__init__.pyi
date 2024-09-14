from typing import Dict, Any, Union, Callable, TypeAlias, Optional, List
from typing_extensions import Self  # for Python <3.11

# Define a type alias for the extraction dictionary
ExtractionDict: TypeAlias = Dict[str, Union[str, Callable[[str], Any]]]

class Fetch:
    def __init__(self, url: str) -> None:
        ...
    
    def query(self, selector: str, key: Optional[str] = None) -> Self:
        ...
    
    def extract(self, extraction: ExtractionDict) -> Self:
        ...
    
    def limit(self, limit: int) -> Self:
        ...
    
    def get_data(self) -> Union[List[Any], List[List[Any]]]:  # Returns a list or a nested list
        ...
    
    def count(self) -> int:
        ...
    
    def __getitem__(self, index: int) -> List[Any]:  # Always returns a list
        ...
    
    def __len__(self) -> int:
        ...
    
    def __repr__(self) -> str:
        ...
    
    def __str__(self) -> str:
        ...