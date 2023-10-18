from fastapi import FastAPI

app = FastAPI()

clients = {}

order = {}

cars = {}


@app.get('/{vin}}/{brand}/{model}/{year}')
def append_cars(brand: str, model: str, year: int, vin: int):
    cars[str(vin)] = {"Model": model, "Brand": brand, "Year": year}
    return "202", {model: cars[str(vin)]}


@app.get('/delete/{vin}')
def delete_car(vin: int):
    del cars[str(vin)]


@app.get('/read/car/{vin}')
def read_data_car(vin: int):
    return cars[str(vin)]