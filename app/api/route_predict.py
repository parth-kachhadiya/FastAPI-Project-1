from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Literal
from app.core.dependencies import getAPIKey, getCurrentUser
from app.services.model_service import predictPrice

Brand = Literal[
    "Maruti", "Hyundai", "Honda", "Mahindra", "Toyota", "Ford",
    "Volkswagen", "Renault", "BMW", "Tata", "Mercedes-Benz", "Skoda",
    "Audi", "Datsun", "Jaguar", "Land Rover", "Jeep", "Kia", "Porsche",
    "Volvo", "MG", "Mini", "Nissan", "Lexus", "Isuzu", "Bentley",
    "Maserati", "ISUZU", "Ferrari", "Mercedes-AMG", "Rolls-Royce", "Force",
]

Model = Literal[
    "i20", "Swift Dzire", "Swift", "Alto", "City", "Wagon R", "Grand",
    "Innova", "Verna", "i10", "Ecosport", "Polo", "Baleno", "Amaze",
    "Ciaz", "Ertiga", "Creta", "XUV500", "KWID", "Vitara", "Scorpio",
    "Figo", "Vento", "Celerio", "Duster", "Bolero", "Fortuner", "Rapid",
    "Jazz", "3", "Tiago", "Santro", "Eeco", "E-Class", "C-Class", "5",
    "WR-V", "Safari", "A4", "Superb", "GO", "Nexon", "RediGO", "Ignis",
    "KUV", "Aspire", "A6", "Thar", "Civic", "Octavia", "Venue", "X1",
    "XF", "Rover", "Elantra", "Endeavour", "Hexa", "Compass", "Tigor",
    "7", "S-Class", "Camry", "GL-Class", "Freestyle", "Seltos", "CR-V",
    "KUV100", "X5", "Marazzo", "Q7", "X3", "Harrier", "Hector", "6",
    "Cooper", "Dzire VXI", "Yaris", "Cayenne", "XUV300", "S-Presso",
    "Triber", "GLS", "Tucson", "redi-GO", "CLS", "Kicks", "Glanza",
    "D-Max", "XL6", "XC", "Z4", "ES", "X4", "A8", "XC60", "S90",
    "Dzire ZXI", "XC90", "XE", "Carnival", "Continental", "CR", "F-PACE",
    "MUX", "X-Trail", "Panamera", "Alturas", "Wrangler", "Dzire LXI",
    "Macan", "NX", "RX", "Aura", "Ghibli", "GTC4Lusso", "Altroz", "C",
    "Ghost", "Quattroporte", "Gurkha",
]

class Car(BaseModel):
    brand             : Brand
    model             : Model
    vehicle_age       : int
    km_driven         : int
    mileage           : float
    engine            : int
    max_power         : float
    seats             : int
    transmission_type : Literal["Manual", "Automatic"]
    seller_type       : Literal["Dealer", "Individual", "Trustmark Dealer"]
    fuel_type         : Literal["Petrol", "Diesel", "CNG", "LPG", "Electric"]


router = APIRouter()


@router.post('/predict')
def makePrediction(data : Car, user = Depends(getCurrentUser), _ = Depends(getAPIKey)):
    prediction = predictPrice(data.model_dump())
    return {
        'predicted_price' : f'{prediction:,.2f}'
    }