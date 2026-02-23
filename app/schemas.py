from pydantic import BaseModel, Field, conint, confloat

class HouseFeatures(BaseModel):
    OverallQual: conint(ge=1, le=10) = Field(..., description="Overall material and finish quality (1-10)")
    GrLivArea: conint(ge=0) = Field(..., description="Above grade (ground) living area square feet")
    GarageCars: conint(ge=0) = Field(..., description="Size of garage in car capacity")
    GarageArea: conint(ge=0) = Field(..., description="Size of garage in square feet")
    TotalBsmtSF: conint(ge=0) = Field(..., description="Total square feet of basement area")

