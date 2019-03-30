import sqlalchemy
from faker import Faker
from faker.providers import profile
from faker.providers import person

N = 100


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


def fill_candidates(candidates, con):
    for _ in range(N):
        fake = Faker()
        fake.add_provider(profile)
        data = fake.profile(fields=None, sex=None)
        clause = candidates.insert().values(name=data.get('name'), surname=data.get('name'))
        con.execute(clause)


def fill_candidates_info(candidates_info, con):
    for _ in range(N):
        fake = Faker()
        fake.add_provider(profile)
        data = fake.profile(fields=None, sex=None)

        gender = data.get('sex')
        current_gender = 0
        if gender == 'M':
            current_gender = 1
        clause = candidates_info.insert().values(nationality='russian', gender=current_gender, age=20,
                                                 email=data.get('mail'))
        con.execute(clause)


def fill_staff(staff, con):
    for _ in range(N):
        fake = Faker()
        fake.add_provider(profile)
        fake.add_provider(person)
        name = fake.first_name()
        surname = fake.last_name()

        clause = staff.insert().values(name=name, surname=surname)
        con.execute(clause)


def fill_staff_position(staffs_position, con):
    for _ in range(N):
        fake = Faker()
        fake.add_provider(profile)
        data = fake.profile(fields=None, sex=None)
        job = data.get('job')

        clause = staffs_position.insert().values(position=job)
        con.execute(clause)


con, meta = connect('postgres', 'qwerty987', 'admissionDB')

tables = meta.tables
candidates = tables.get('candidates')
candidates_info = tables.get('candidates_info')
staff = tables.get('staff')
staffs_position = tables.get('staffs_position')
managers = tables.get('managers')

# fill_candidates(candidates, con)
# fill_candidates_info(candidates_info, con)

# fill_staff(staff, con)
# fill_staff_position(staffs_position,con)
# fill_staff(managers, con)
