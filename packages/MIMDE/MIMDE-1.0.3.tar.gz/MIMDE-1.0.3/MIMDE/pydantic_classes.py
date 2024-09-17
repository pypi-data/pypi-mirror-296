import json
from typing import List, Optional, Dict
from pydantic import BaseModel, validator


#------------------------ Low Level Analysis ------------------------#
class LowLevelTheme(BaseModel):
    theme: str

class OutlierCategory(BaseModel):
    irrelevant: bool
    incoherent: bool
    extreme: bool
    other: bool

class Outlier(BaseModel):
    is_outlier: bool
    outlier_category: OutlierCategory
    outlier_reason: Optional[str] = None
    outlier_score: Optional[float] = 0.0
    # Set outlier_score to 0.0 if it is None or not a number
    @validator('outlier_score', pre=True)
    def set_outlier_score(cls, v):
        if v is None or not isinstance(v, (int, float)):
            return 0.0
        return float(v)

class LowLevelResponseAnalysis(BaseModel):
    themes: List[LowLevelTheme]
    mcq_contradiction: bool = False
    outlier: Outlier
#-------------------------------------------------------------------#



#--------------------- Rough High Level Analysis -------------------#
class RoughHighLevelTheme(BaseModel):
    theme: str

class RoughHighLevelAnalysis(BaseModel):
    themes: List[RoughHighLevelTheme]
#-------------------------------------------------------------------#



#----------------------- High Level Analysis -----------------------#

class HighLevelTheme(BaseModel):
    cluster_n: int
    theme: str
    # Set validator to ensure that cluster_n is an integer and transform a str to an int
    @validator('cluster_n')
    def cluster_n_must_be_int(cls, v):
        if not isinstance(v, int):
            return int(v)
        return v

class HighLevelResponseAnalysis(BaseModel):
    themes: List[HighLevelTheme]
