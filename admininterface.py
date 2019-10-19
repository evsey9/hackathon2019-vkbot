import dataset
import PyQt5
db = dataset.connect('sqlite:///botdatabase.db')

table_teachers = db['teachers']
table_timetable = db['timetable']
table_addresses = db['addresses']

