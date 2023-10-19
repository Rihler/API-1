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
        if not(self.brand.isalpha()) or not(self.valid_sym(self.brand)):
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

@app.post('/car')
def append_car(vin, brand, model, year):
    car = Car(vin, model, brand, year)
    car.valid_car()
    for i in car.errors:
        if car.errors[i] != "valid":
            return car.errors
    return post_data(vin, model.lower(), brand.lower(), year, "Model", "Brand", "Year", cars, 0)


@app.delete('/delete/car')
def delete_car(vin):
    return delete_data(vin, cars)


@app.get('/read/car')
def read_data_car(vin):
    if vin in cars:
        return {vin: cars[vin]}
    return "Данного автомобиля не существует"


@app.put("/update/car")
def update_data_car(vin, brand, model, year):
    car = Car(vin, brand, model, year)
    car.valid_car()
    for i in car.errors:
        if car.errors[i] != "valid":
            return car.errors
    return post_data(vin, model.lower(), brand.lower(), year, "Model", "Brand", "Year", cars, 1)


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
            self.errors["phone"] = "Номер должен начинаться с + и содержать 11 цифр"

        if not(self.valid_sym(self.name)) or not(self.name.isalpha()) or len(self.name) < 3:
            self.errors["name"] = "Имя не должно содержать спец. символы и цифры, длина имени 3 сим. минимум"

        if not(self.valid_sym(self.second_name)) or not(self.second_name.isalpha()) or len(self.second_name) < 3:
            self.errors["second_name"] = "Фамилия не должна содержать спец. символы и цифры, длина фамилии 3 сим. минимум"

        if len(self.address) < 10:
            self.errors["address"] = "Адрес должен содержать не менее 10 символов"

@app.post("/people")
def append_people(phone, name, second_name, address):
    pep = People(phone, name, second_name, address)
    pep.valid_people()
    for i in pep.errors:
        if pep.errors[i] != "valid":
            return pep.errors
    return post_data(phone, name, second_name, address, "Name", "Second_name", "Address", peoples, 0)


@app.delete("/delete/people")
def delete_people(phone):
    return delete_data(phone, peoples)


@app.get("/read/people")
def read_data_peoples(phone):
    if phone in peoples:
        return {phone: peoples[phone]}
    return "Данного пользователя не существует"


@app.put("/update/people")
def update_data_people(phone, name, second_name, address):
    pep = People(phone, name, second_name, address)
    pep.valid_people()
    for i in pep.errors:
        if pep.errors[i] != "valid":
            return pep.errors
    return post_data(phone, name, second_name, address, "Name", "Second_name", "Address", peoples, 1)

orders = []

people_car={}

class Order(object):
    def __init__(self, phone, vin, date="10.12.2023", work="что - то", status='завершен'):
            self.lst_status = ["завершен", "в процессе", "ожидает ремонта"]
            self.phone = phone
            self.vin = vin.upper()
            self.date = date
            self.work = work.lower()
            self.status = status.lower()
            self.errors = {"phone": "valid", "vin": "valid", "date": "valid", "work": "valid", "status": "valid"}
    def valid_sym(self, string):
        error_syms = "_/€&#@%~;:|[] <>{}^*-+=(),"
        for x in error_syms:
            if x in string:
                return False
        return True

    def valid_order(self):
        if not (self.phone[1:].isdigit()) or len(self.phone[1:]) != 11 or self.phone[0] != "+" or not (
        self.valid_sym(self.phone[1:])):
            self.errors["phone"] = "Номер должен начинаться с + и содержать 11 цифр"

        if len(self.vin) != 17 or "I" in self.vin or "O" in self.vin or "Q" in self.vin or not (
                self.valid_sym(self.vin)):
            self.errors["vin"] = "Vin код не должен содержать I, Q, O и спец. знаков\
 и его длина должна быть 17 символов"

        if self.status not in self.lst_status:
            self.errors["status"] = 'Статус может быть только \"завершен\", \"в процессе\", \"ожидает ремонта\" '

        date1= self.date.replace(" ","").split(".")
        if len(date1) != 3:
            self.errors["date"] = "Дата должна иметь формат день.номер_месяца.год"
        if len(date1) == 3:
            if not(date1[0].isdigit()) or not(date1[1].isdigit()) or not(date1[2].isdigit()):
                self.errors["date"] = "Дата должна иметь формат день.номер_месяца.год"
        if len(date1) == 3 and date1[0].isdigit() and date1[1].isdigit() and date1[0].isdigit():
            if not(1<=int(date1[0]) <= 31) or (1<=(date1[1]) <=12) or  not(1950 <= date1[2] <=2023):
                self.errors["date"] = "Месяц должен быть в пределах (1, 31), месяц - (1,12), год - (1950, 2023)"
@app.post("/order")
def append_order(phone, vin, date, work, status):
    order = Order(phone, vin, date, work, status)
    for i in order.errors:
        if order.errors[i] != "valid":
            return order.errors
    st = {phone: {"vin": vin, "date": date, "work": work, "status": status}}
    a = []
    for x in orders:
        for y in x:
            a.append(x[y]["vin"])
        if vin in a:
            return "Заказ на данный автомобиль уже существует"
    if st not in orders:
        orders.append(st)
        if phone in people_car:
            people_car[phone]. append(vin)
        else:
            people_car[phone] = [vin]
        return st
    return "Данный заказ уже существует"


@app.delete("/delete/order")
def delete_order(phone, vin):
    order = Order(phone, vin)
    for i in order.errors:
        if order.errors[i] != "valid":
            return order.errors
    order1 = 0
    for x in orders:
        for y in x:
            if [x[y]["vin"], y] == [vin, phone]:
                order1 = x
    if order1 != 0:
        orders.remove(order1)
        return "order is deleted"
    return "Данного заказа нет в базе данных"


@app.put("/update/order")
def update_order(phone, vin, status):
    order = Order(phone, vin)
    for i in order.errors:
        if order.errors[i] != "valid":
            return order.errors
    order1 = 0
    for x in orders:
        for y in x:
            if [x[y]["vin"], y] == [vin, phone]:
                order1 = x
    if order1 != 0:
        order1[phone]["status"] = status
        return "order is update"
    return "Данного заказа нет в базе данных"



@app.get("/read/order")
def read_data_order(phone, vin):
    for x in orders:
        for y in x:
            if y == phone and x[y]["vin"] == vin:
                return {y: x[y]}
    return "Данного закаказа нет"

@app.get("/read/people_car")
def read_pep_car(phone):
    if phone not in people_car:
        return "Данного пользователя нет"
    else:
        return {phone: people_car[phone]}

@app.get("/read/people_order")
def read_pep_order(phone):
    a = []
    for x in orders:
        for y in x:
            if y == phone:
                a.append(x)
    if len(a) != 0:
        return a
    return "Заказов на данного пользователя нет"
