class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = False

    SECRET_KEY = 'some-secret-string'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ssd_project@35.243.196.1/admission_db'
    JWT_SECRET_KEY = 'jwt-secret-string'

    STATIC_URL_PATH = '/static'
    STATIC_FOLDER = 'public'


API_VERSION_NUMBER = '0.0.7'
API_VERSION_LABEL = 'v1'

OPENAPI_META = """
    openapi: 3.0.2
    info:
        description: 'IU admission portal backend API (prototype)'
        title: 'Admission Portal'
        version: {}
    tags:
        - name: Auth
        - name: Profile
        - name: Tests
        - name: Submissions
        - name: Service
    servers:
        - url: /
    components:
        examples:
            Registration:
                email: super@innopolis.ru
                password: 123456
                name: Super
                surname: Innopolis
            ProfileFull:
                user:
                  first_name:
                  last_name:
                  role:
                authentication:
                  email:
                info:
                  skype:
                  subscription_email:
                  gender:
                  date_of_birth:
                  phone:
                  nationality:
                documents:
                  cv:
                  passport:
                  transcript:
                  project_description:
                  photo:
                  motivation_letter:
                  letter_of_recommendation:
                status:
                  status:
""".format(API_VERSION_NUMBER)

SPEC_FILENAME = 'spec.json'
