import dataset
import PyQt5

db = dataset.connect('sqlite:///botdatabase.db')
try:
    db['teachers'].drop()
    db['groups'].drop()
    db['locations'].drop()
except:
    pass
teachers = db['teachers']
groups = db['groups']
locations = db['locations']

teachers.insert(dict(lastname="Нугманов", firstname="Имя", middlename="Отчество", # 1
                           phone="89526664848", mail="mail@mail.ru", age=21))
teachers.insert(dict(lastname="Кураш", firstname="Имя", middlename="Отчество", # 2
                           phone="89526664848", mail="mail@mail.ru", age=21))
teachers.insert(dict(lastname="Шабалин", firstname="Имя", middlename="Отчество", # 3
                           phone="89526664848", mail="mail@mail.ru", age=21))
teachers.insert(dict(lastname="Зырянов", firstname="Имя", middlename="Отчество", # 4
                           phone="89526664848", mail="mail@mail.ru", age=21))
teachers.insert(dict(lastname="Шульга", firstname="Имя", middlename="Отчество", # 5
                           phone="89526664848", mail="mail@mail.ru", age=21))
teachers.insert(dict(lastname="Валеев", firstname="Имя", middlename="Отчество", # 6
                           phone="89526664848", mail="mail@mail.ru", age=21))


groups.insert(dict(location_id=1, time_start="15:00", time_end="17:00",
                         days="1 3 4", teacher=1))

groups.insert(dict(location_id=2, time_start="10:00", time_end="12:00",
                         days="2 4 5", teacher=2))
groups.insert(dict(location_id=2, time_start="10:00", time_end="12:00",
                         days="3", teacher=3))
groups.insert(dict(location_id=2, time_start="15:00", time_end="17:00",
                         days="4 5", teacher=3))


groups.insert(dict(location_id=3, time_start="10:00", time_end="12:00",
                         days="1 3", teacher=2))
groups.insert(dict(location_id=3, time_start="15:00", time_end="17:00",
                         days="1 2", teacher=4))
groups.insert(dict(location_id=3, time_start="14:30", time_end="16:30",
                         days="5", teacher=4))

groups.insert(dict(location_id=4, time_start="15:00", time_end="17:00",
                         days="1 2 3 4 5", teacher=5))

groups.insert(dict(location_id=5, time_start="9:00", time_end="17:00",
                         days="1", teacher=6))
groups.insert(dict(location_id=5, time_start="10:00", time_end="12:00",
                         days="3", teacher=6))
groups.insert(dict(location_id=5, time_start="15:00", time_end="17:00",
                         days="3 4 5", teacher=6))

groups.insert(dict(location_id=6, time_start="13:00", time_end="15:00",
                         days="6", teacher=1))




locations.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="34 лицей", latitude=57.131320,
                            longitude=65.589212))
locations.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="92 СОШ", latitude=57.131320,
                            longitude=65.589212))
locations.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="81 лицей", latitude=57.131320,
                            longitude=65.589212))
locations.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="88 СОШ", latitude=57.131320,
                            longitude=65.589212))
locations.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="1 гимназия", latitude=57.131320,
                            longitude=65.589212))
locations.insert(dict(country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="Технопарк", latitude=57.131320,
                            longitude=65.589212))
#testing