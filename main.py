from fastapi import FastAPI

app = FastAPI()

clients = {}

order = {}

cars = {}


@app.post('/car/{vin}/{brand}/{model}/{year}')
def append_car(vin: int, model: str, brand: str, year: int):
    cars[str(vin)] = {"Model": model, "Brand": brand, "Year": year}
    return "202", {str(vin): cars[str(vin)]}


@app.delete('/delete/{vin}')
def delete_car(vin: int):
    if str(vin) in cars.keys():
        vin1 = vin
        del cars[str(vin)]
        return f"202, {vin1} is deleted"
    return f"{vin} does not exist in the database"

@app.get('/read/cars/')
def read_data_car():
    return cars


@app.put("/update/car/{vin}/")
def update_data_car(vin: int, model: str, brand: str, year: int):
    if str(vin) in cars.keys():
        cars[str(vin)] = {"Model": model, "Brand": brand, "Year": year}
        return "202", {model: cars[str(vin)], "vin": vin}
    return f"{vin} does not exist in the database"
