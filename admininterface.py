import dataset
import PyQt5

db = dataset.connect('sqlite:///botdatabase.db')

table_teachers = db['teachers']
table_groups = db['groups']
table_addresses = db['addresses']

table_teachers.insert(dict(id=1, lastname="Фамилия", firstname="Имя", middlename="Отчество",
                           phone="89526664848", mail="mail@mail.ru", age=21))

# table_groups.insert(dict(school = "Школа", monday = "10:00-18:00", mondayteacher = 0, tuesday = "10:00-18:00",
# tuesdayteacher = 0, wednesday = "10:00-18:00", wednesdayteacher = 0, thursday = "10:00-18:00", thursdayteacher = 0,
# friday = "10:00-18:00", fridayteacher = 0, saturday = "10:00-18:00", saturdayteacher = 0))
table_groups.insert(dict(id=1, location_id=1, day=1, time_start="10:00", time_end="18:00",
                         days="1, 3", teacher=1))

table_addresses.insert(dict(id=1, country="Россия", region="Тюменская область", city="Тюмень",
                            street="улица Рижская", building="71", name="Гимназия №16", latitude=57.131320,
                            longitude=65.589212))
