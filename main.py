from fastapi import FastAPI

app = FastAPI()

cars = {}


def delete_data(key, dict_keys):
    if key in dict_keys.keys():
        key1 = key
        del dict_keys[key]
        return f"202, {key} is deleted"
    return f"{key} does not exist in the database"


def post_data(par1, par2, par3, par4, key2, key3, key4, dict_data, put):
    if put == 0:
        if par1 not in dict_data.keys():
            dict_data[par1] = {f"{key2}": par2, f"{key3}": par3, f"{key4}": par4}
            return "202", {par1: dict_data[par1]}
        return f"{par1} already exists"
    if put == 1:
        if par1 in dict_data.keys() and put == 1:
            dict_data[par1] = {f"{key2}": par2, f"{key3}": par3, f"{key4}": par4}
            return "202", {par1: dict_data[par1]}
        return f"{par1} does not exist in the database"


class Car(object):
    def __init__(self, vin, model=None, brand=None, year=None):
        self.vin = vin.upper()
        self.model = model
        self.brand = brand
        self.year = year
        self.errors = {"vin": "valid", "model": "valid", "brand": "valid", "year": "valid"}

    def valid_sym(self, string):
        error_syms = "_/€&#@%~;:|[] <>{}^*-+=()"
        for x in error_syms:
            if x in string:
                return False
        return True

    def valid_car(self):
        if len(self.vin) != 17 or "I" in self.vin or "O" in self.vin or "Q" in self.vin or not (
                self.valid_sym(self.vin)):
            self.errors["vin"] = "Vin код не должен содержать I, Q, O и спец. знаков\
 и его длина должна быть 17 символов"
        if not (self.brand.isdigit()) or not (self.brand[0].isalpha()) or not (self.valid_sym(self.brand)):
            self.errors["brand"] = "Марка не должна содержать спец.\
символы и цифры и не должна начинаться с цифр "
        flag = True
        if not (self.year.isdigit()):
            self.errors["year"] = "Год должен быть числом от 1950 до 2023 включительно"
            flag = False
        if flag:
            if not (1950 < int(self.year) <= 2023):
                self.errors["year"] = "Год должен быть числом от 1950 до 2023 включительно"
        if not (self.valid_sym(self.model)):
            self.errors["vin"] = "Модель не должна содержать спец. символы"


# CRUD для автомобилей

@app.post('/car/{vin}/{brand}/{model}/{year}')
def append_car(vin, brand, model, year):
    car = Car(vin, model, brand, year)
    car.valid_car()
    for i in car.errors:
        if car.errors[i] != "valid":
            return car.errors
    return post_data(vin, model.lower(), brand.lower(), year, "Model", "Brand", "Year", cars, 0)


@app.delete('/delete/car/{vin}')
def delete_car(vin):
    return delete_data(vin, cars)


@app.get('/read/cars/')
def read_data_car():
    return cars


@app.put("/update/car/{vin}/")
def update_data_car(vin, brand, model, year):
    car = Car(vin, brand, model, year)
    car.valid_car()
    for i in car.errors:
        if car.errors[i] != "valid":
            return car.errors
    return post_data(vin, model.lower(), brand.lower(), year, "Model", "Brand", "Year", cars, 0)


peoples = {}

class People(object):
    def __init__(self, phone, name=None, second_name=None, address=None):
        self.phone = phone
        self.name = name.capitalize()
        self.second_name = second_name.capitalize()
        self.address = address.capitalize()
        self.errors = {"phone": "valid", "name": "valid", "second_name": "valid", "address": "valid"}

    def valid_sym(self, string):
        error_syms = "_/€&#@%~;:|[] <>{}^*-+=(),"
        for x in error_syms:
            if x in string:
                return False
        return True

    def valid_people(self):
        if not(self.phone[1:].isdigit()) or len(self.phone[1:]) != 11 or self.phone[0] != "+" or not(self.valid_sym(self.phone[1:])):
            self.errors["phone"] = "Номер должен начинаться с + и содержать 10 цифр"

        if not(self.valid_sym(self.name)) or not(self.name.isalpha()) or len(self.name) < 3:
            self.errors["name"] = "Имя не должно содержать спец. символы и цифры, длина имени 3 сим. минимум"

        if not(self.valid_sym(self.second_name)) or not(self.second_name.isalpha()) or len(self.second_name) < 3:
            self.errors["second_name"] = "Фамилия не должна содержать спец. символы и цифры, длина фамилии 3 сим. минимум"

        if len(self.address) < 10:
            self.errors["address"] = "Адрес должен содержать не менее 10 символов"

@app.post("/people/{phone}/{name}/{second_name}/{address}/")
def append_people(phone, name, second_name, address):
    pep = People(phone, name, second_name, address)
    pep.valid_people()
    for i in pep.errors:
        if pep.errors[i] != "valid":
            return pep.errors
    return post_data(phone, name, second_name, address, "Name", "Second_name", "Address", peoples, 0)


@app.delete("/delete/people/{phone}")
def delete_people(phone):
    return delete_data(phone, peoples)


@app.get("/read/peoples")
def read_data_peoples():
    return peoples


@app.put("/update/people/{phone}/{name}/{second_name}/{address}/")
def update_data_people(phone, name, second_name, address):
    pep = People(phone, name, second_name, address)
    pep.valid_people()
    for i in pep.errors:
        if pep.errors[i] != "valid":
            return pep.errors
    return post_data(phone, name, second_name, address, "Name", "Second_name", "Address", peoples, 1)
