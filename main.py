from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

clients = {}

order = {}

cars = {}


# CRUD для автомобилей
def valid_brand(brand):
    return any(map(str.isdigit, brand))

@app.post('/car/{vin}/{brand}/{model}/{year}')
def append_car(vin: int = Path(lt=10 ** 18, ge=10 * 17), model: str = Path(min_length=4, max_length=8),
               brand: str = Path(min_length=4, max_length=8), year: int = Path(lt=2023, ge=1950)):
    if valid_brand(brand):
        return "Brand doesnt include numbers"
    if str(vin) not in cars.keys():
        cars[str(vin)] = {"Model": model.lower(), "Brand": brand.lower(), "Year": year}
        return "202", {str(vin): cars[str(vin)]}
    return f"{vin} already exists"


@app.delete('/delete/{vin}')
def delete_car(vin: int = Path(lt=10 ** 18, ge=10 * 17)):
    if str(vin) in cars.keys():
        vin1 = vin
        del cars[str(vin)]
        return f"202, {vin1} is deleted"
    return f"{vin} does not exist in the database"


@app.get('/read/cars/')
def read_data_car():
    return cars


@app.put("/update/car/{vin}/")
def update_data_car(vin: int = Path(lt=10 ** 18, ge=10 * 17), model: str = Path(min_length=4, max_length=8),
                    brand: str = Path(min_length=4, max_length=8), year: int = Path(lt=2023, ge=1950)):
    if str(vin) in cars.keys():
        if valid_brand(brand):
            return "Brand doesnt include numbers"
        cars[str(vin)] = {"Model": model, "Brand": brand, "Year": year}
        return "202", {model: cars[str(vin)], "vin": vin}
    return f"{vin} does not exist in the database"
