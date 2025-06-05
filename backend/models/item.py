from pydantic import BaseModel

class Item(BaseModel):
    article_id: int
    prod_name: str
    prod_type_name: str
    prod_group_name: str
    graphical_appearance_name: str
    colour_group_name: str
    perceived_colour_value_name: str
    perceived_colour_master_name: str
    index_group_name: str
    garment_group_name: str
    detail_desc: str
    sleeve_prediction: str
    length_prediction: str
    neckline_prediction: str
    detected_fabrics: str

class RecItem(Item):
    # Recommendation scores
    compatibility_score: float = 0.0
    
    # Feature importance scores (existing)
    color_importance: float = 0.0
    luminance_importance: float = 0.0
    appearance_importance: float = 0.0
    fabric_importance: float = 0.0
    neckline_importance: float = 0.0
    sleeve_importance: float = 0.0
    length_importance: float = 0.0