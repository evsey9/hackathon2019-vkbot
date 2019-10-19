import dataset
import PyQt5

db = dataset.connect('sqlite:///botdatabase.db')
try:
    db['teachers'].drop()
    db['groups'].drop()
    db['addresses'].drop()
except:
    pass
teachers = db['teachers']
groups = db['groups']
addresses = db['addresses']

teachers.insert(dict(lastname="Охметович", firstname="Имя", middlename="Отчество",
                           phone="89526664848", mail="mail@mail.ru", age=21))

groups.insert(dict(location_id=1, day=1, time_start="10:00", time_end="18:00",
                         days="1, 3", teacher=1))

addresses.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="Гимназия №16", latitude=57.131320,
                            longitude=65.589212))

#testing