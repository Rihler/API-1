from fastapi import FastAPI, Path

app = FastAPI()

clients = {}

order = {}

cars = {}


class Car(object):
    def _init_(self, vin, model, brand, year):
        self.vin = vin
        self.model = model
        self.brand = brand
        self.year = year
        self.errors = {"vin": "valid", "model": "valid", "brand": "valid", "year": "valid"}

    def valid_sym(self, string):
        error_syms = "_/€&#@ %~;:|[] <>{} *-+=()"
        for x in error_syms:
            if x in string:
                return False
        return True

    def valid_car(self):
        if len(self.vin) != 17 or "I" in self.self.vin or "O" in self.vin or "Q" in self.vin or not (self.valid_sym(self.vin)):
            self.errors["vin"] = "Vin код не должен содержать I, Q, O и спец. знаков\
             и его длина должна быть 17 символов"
        if self.brand.isdigit() or not (self.brand[0].isalpha()) or not (self.valid_sym(self.brand)):
            self.errors["brand"] = "Марка не должна содержать спец.\
             символы и цифры и не должна начинаться с цифр "
        if not(self.year.isdigit()) and not (1950 < int(self.year) <= 2023):
            self.errors["year"] = "Год должен быть числом от 1950 до 2023 включительно"
        if not (self.valid_sym(self.model)):
            self.errors["vin"] = "Модель не должна содержать спец. символы"


# CRUD для автомобилей

@app.post('/car/{vin}/{brand}/{model}/{year}')
def append_car(vin, brand, model, year):
    car = Car(vin = vin, model = model, brand = brand, year = year)
    car.valid_car()

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
