from typing import Set, List, Optional, Tuple

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Date, Boolean, Text, BigInteger, ForeignKey, ForeignKeyConstraint, \
    UniqueConstraint, Numeric, Enum, ARRAY
from sqlalchemy.orm import relationship, sessionmaker, Session, scoped_session
from datetime import date, datetime
from server import application

db = application.db


class RevokedToken(db.Model):
    """
    Storage of the token required for authentification
    """
    __tablename__ = 'revoked_tokens'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    jti = Column(Text())
    date = Column(Date)
    expires = Column(Date)
    revoked = Column(Boolean, default=False)
    token_type = Column(Text)
    user_id = Column(BigInteger)


class Users(db.Model):
    """
    Keeps the general info about candidates such as Name, Surname and id
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    role = Column(BigInteger)

    autorization = relationship('UsersAutorization', cascade="all,delete", backref='user',
                                uselist=False)  # one-to-one
    info = relationship('CandidatesInfo', cascade="all,delete", backref='user', uselist=False)  # one-to-one
    status = relationship('CandidatesStatus', cascade="all,delete", backref='user', uselist=False)  # one-to-one
    documents = relationship('CandidatesDocuments', cascade="all,delete", backref='user',
                             uselist=False)  # one-to-one
    # tests = relationship('CandidatesAnswers', cascade="all,delete", backref='user', uselist=False)  # one-to-one # todo: check
    submission = relationship('TestsSubmissions', cascade="all,delete", backref='user',
                              uselist=False)  # one-to-one
    candidates_interview = relationship('CandidatesInterview', cascade="all,delete", backref='candidate',
                                        primaryjoin="Users.id == CandidatesInterview.candidate_id",
                                        uselist=False)  # one-to-one
    staff_interview = relationship('CandidatesInterview', cascade="all,delete", backref='staff',
                                   primaryjoin="Users.id == CandidatesInterview.staff_id", uselist=False)  # one-to-one
    staff_positions = relationship('Staff', cascade="all,delete", backref='user',
                                   uselist=False)  # one-to-one


class Staff(db.Model):
    """
    Keeps id of users with the manager of professor role and their positions
    """
    __tablename__ = 'staff'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey(Users.id), primary_key=True)
    position = Column(Text)


class UsersAutorization(db.Model):
    """
    Keeps data email and password for candidates' authorization
    """
    __tablename__ = 'candidates_autorization'
    __table_args__ = {'extend_existing': True}

    email = Column(Text, primary_key=True)
    id = Column(BigInteger, ForeignKey(Users.id), unique=True)  # one to one
    password = Column(Text)


class CandidatesInfo(db.Model):
    """
    Keeps info about each candidate such as nationality, gender, date of birth and email
    """
    __tablename__ = 'candidates_info'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey(Users.id), primary_key=True)  # one-to-one
    nationality = Column(Text)
    gender = Column(Boolean)
    date_of_birth = Column(Date)
    subscription_email = Column(Text)
    skype = Column(Text)
    phone = Column(Text)


class CandidatesInterview(db.Model):
    """
    Keeps data about candidate, interviewer and date of an interview
    """
    __tablename__ = 'candidates_interview'
    __table_args__ = {'extend_existing': True}

    candidate_id = Column(BigInteger, ForeignKey(Users.id), primary_key=True)
    staff_id = Column(BigInteger, ForeignKey(Users.id), primary_key=True)
    interview_date = Column(Date)


class CandidatesDocuments(db.Model):
    """
    Keeps link on candidate's documents
    """
    __tablename__ = 'candidates_documents'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey(Users.id), primary_key=True)  # one-to-one
    cv = Column(Text)
    letter_of_recommendation = Column(Text)
    motivation_letter = Column(Text)
    passport = Column(Text)
    photo = Column(Text)
    project_description = Column(Text)
    transcript = Column(Text)


class CandidatesStatus(db.Model):
    """
    Keeps info about candidate's status which is integer according to accepted/rejected/waiting_list
    """
    __tablename__ = 'candidates_status'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey(Users.id), primary_key=True)  # one-to-one
    status = Column(BigInteger)
    admission_date = Column(Date)


class TestsSubmissions(db.Model):
    """
    Keeps data about tests that were submitted or started by a candidate
    """
    __tablename__ = 'candidates_submissions'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    candidate_id = Column(BigInteger, ForeignKey(Users.id))
    time_start = Column(Date, default=datetime.utcnow)
    time_end = Column(Date)
    submitted = Column(Boolean)
    graded_by = (BigInteger, ForeignKey(Users.id))

    answers = relationship('CandidatesAnswers', cascade="all,delete", backref='questions_tests',
                           uselist=False)


class Questions(db.Model):
    """
    Keeps all questions according to all tests in the system
    """
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    question = Column(Text)
    question_type = Column(BigInteger)
    answer = Column(Text)
    manually_grading = Column(Boolean, default=False)
    points = Column(BigInteger)

    test = relationship('QuestionsTests', cascade="all,delete", backref='questions',
                        primaryjoin="Questions.id == QuestionsTests.question_id", uselist=False)
    # candidates_answers = relationship('CandidatesAnswers', cascade="all,delete", backref='questions_tests', # todo: is required?
    # uselist=False)  # one-to-one


class CandidatesAnswers(db.Model):
    """
    Keeps info about tests that were passed by candidate
    """
    __tablename__ = 'candidates_answers'
    __table_args__ = {'extend_existing': True}

    # composite primary key
    submission_id = Column(BigInteger, ForeignKey(TestsSubmissions.id), primary_key=True)  # one-to-one
    question_id = Column(BigInteger, ForeignKey(Questions.id), primary_key=True)
    answer = Column(ARRAY(Text))
    grade = Column(Numeric)
    comments = Column(Text)


class Tests(db.Model):
    """
    All actual and archived tests in the system
    """
    __tablename__ = 'tests'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    test_name = Column(Text)
    max_time = Column(Date)
    archived = Column(Boolean)

    questions_tests = relationship('QuestionsTests', cascade="all,delete", backref='tests',
                                   uselist=False)  # one-to-one
    # questions = relationship('Questions', cascade="all,delete", backref='questions_tests', # todo: is required?
    # uselist=False)  # one-to-one


class QuestionsTests(db.Model):
    """
    Linking table between tests and questions
    """
    __tablename__ = 'questions_tests'
    __table_args__ = {'extend_existing': True}

    question_id = Column(BigInteger, ForeignKey(Questions.id), primary_key=True)
    test_id = Column(BigInteger, ForeignKey(Tests.id))


class ORM:
    """
    Supports AddOrUpdate and Remove operations for all the non-associative tables
    Should automatically handle starting/finishing the session
    """

    def __init__(self, db: SQLAlchemy):
        self.session = db.session
        # POSTGRES_ADDRESS = self.get_postgres_address('posgres', 'qwerty987', 'admissionDB', 'localhost', 5432)
        # self.engine = create_engine(POSTGRES_ADDRESS, client_encoding='utf8')
        # self.session = self._get_session()

    # ------------
    # SESSION
    def get_postgres_address(user, password, db, host='localhost', port=5432):
        """Returns a url to connect with PostgreSQL"""

        # We connect with the help of the PostgreSQL URL
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        return url

    def _get_session(self) -> Optional[Session]:
        """Connects to database, and returns Session"""
        try:
            # self.engine = create_engine(POSTGRES_ADDRESS)
            Session = scoped_session(sessionmaker(bind=self.engine))
            self.session = Session()
            return self.session
        except Exception as excpt:
            print(f'Can\'t connect to the database: {excpt}')

    def open_session(self):
        """Opens session"""
        if not self.session:
            self.session = self._get_session()
        else:
            print(f'Session for {self.engine} is already open')

    def close_session(self):
        """Closes session"""
        self.session.commit()
        self.session.close()
        self.session = None

    # ------------
    # ADD
    def add_user(self, first_name: str = None, last_name: str = None) -> Optional[int]:
        """
        Adds new candidate to the database
        """
        try:
            new_candidate = Users(first_name=first_name, last_name=last_name)
            self.session.add(new_candidate)
            self.session.commit()
            return new_candidate
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add new candidate: {excpt}')
        return None

    def add_token(self, jti, date, expires, token_type, user_id, revoked=False) -> Optional[int]:
        try:
            new_token = RevokedToken(jti=jti, date=date, expires=expires, token_type=token_type,
                                     user_id=user_id, revoked=revoked)
            self.session.add(new_token)
            self.session.commit()
            return new_token
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add new token: {excpt}')
        return None

    def add_candidates_info(self, candidate_id, nationaity: str = None, gender: bool = False,
                            date_of_birth: Date = None,
                            subscription_email: str = None, skype: str = None, phone: str = None) -> Optional[int]:
        """
        Adds all necessary candidate's info
        :param candidate_id: id of the given candidate
        :param nationaity: nationality
        :param gender: boolean value. False for male and true for female
        :param date_of_birth: datetime
        :param subscription_email: email used for autorization
        :param skype: skype username
        :param phone: mobile phone of the user
        :return: id of the given candidate or None in case of error
        """
        try:
            candidates_info = CandidatesInfo(candidate_id=candidate_id, nationaity=nationaity, gender=gender,
                                             date_of_birth=date_of_birth,
                                             subscription_email=subscription_email, skype=skype, phone=phone)
            self.session.add(candidates_info)
            self.session.commit()
            return candidates_info.id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add candidates info: {excpt}')
        return None

    def add_candidates_autorization(self, email: str, id: int, password: str) -> Optional[int]:
        """
        Fill in all necessary fields for autorization
        :param email: candidates's email
        :param id: candidate's id
        :param password: candidates's password
        :return: new or existing autorization instance or None in case of error
        """
        try:
            existing_candidates_autorization = self.session.query(UsersAutorization).filter_by(email=email).first()
            if not existing_candidates_autorization:
                candidate_autorization = UsersAutorization(email=email, id=id, password=password)
                self.session.add(candidate_autorization)
                self.session.commit()
                return candidate_autorization
            else:
                return existing_candidates_autorization
        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t add candidates autorization: {excpt}')
        return None

    def add_candidates_documents(self, id: int, cv: str = None, letter_of_recommendation: str = None,
                                 motivation_letter: str = None, passport: str = None, photo: str = None,
                                 project_description: str = None, transcript: str = None) -> Optional[int]:
        """
        Add all necessary candidates documents (links to the files)
        :param id: candidate's id
        :param cv: link to the cv
        :param letter_of_recommendation: link to the letter of recommendation
        :param motivation_letter: link to the motivation letter
        :param passport: link to the scan of the passport
        :param photo: link to the photo of given candidate
        :param project_description: link to the project description
        :param transcript: link to the transcript
        :return: id of the given candidate or None in case of error
        """
        try:
            candidates_documents = CandidatesDocuments(id=id, cv=cv,
                                                       letter_of_recomendation=letter_of_recommendation,
                                                       motivation_letter=motivation_letter, passport=passport,
                                                       photo=photo, project_description=project_description,
                                                       transcript=transcript)
            self.session.add(candidates_documents)
            self.session.commit()
            return candidates_documents.id
        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t add candidates documents: {excpt}')
        return None

    # tests adding
    def add_question(self, question: str, question_type: int, answer: [str], manually_grading: bool, points: float,
                     test_id: int) -> Optional[int]:
        """
        Adds new question to the questions table. Also adds pair question_id, test_id to the question_tests linking
        table.
        :param question: the text of the question including answers to choose
        :param question_type: type of question that maps to single choice, multiple choice and open question
        :param answer: the right answer to this question. If it is open question this field will be empty
        :param manually_grading: true for open questions
        :param points: points that can be earn for this question
        :param test_id: id of the test that includes this question
        :return:
        """
        try:
            new_question = Questions(question=question, question_type=question_type, answer=answer,
                                     manually_grading=manually_grading, points=points)
            new_questions_tests = QuestionsTests(question_id=new_question.id, test_id=test_id)
            self.session.add(new_question)
            self.session.add(new_questions_tests)
            self.session.commit()
            return new_question.id
        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t add question: {excpt}')
        return None

    def add_test(self, test_name: str, max_time: int, archived: bool = False) -> Optional[int]:

        try:
            new_test = Tests(test_name=test_name, max_time=max_time, archived=archived)
            self.session.add(new_test)
            self.session.commit()
            return new_test.id
        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t add test: {excpt}')
        return None

    # ------------
    # GET

    def get_user(self, id: int) -> Optional[Users]:
        """
        Get user's instance by given id
        :param id: id of the user
        :return: user's instances or None if there is no such candidate
        """
        try:
            user = self.session.query(Users).get(id)
            return user
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get user: {excpt}')
        return None

    def get_token(self, id) -> Optional[RevokedToken]:
        """
        Get token's instance by given id
        :param id: id of the token
        :return: token's instances or None if there is no such token
        """
        try:
            token = self.session.query(RevokedToken).get(id)
            return token
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get token: {excpt}')
        return None

    def get_candidate_name_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's name by given id
        :param id: id of the candidate
        :return: candidate's name or None if there is no such candidate
        """
        try:
            candidate = self.session.query(Users).get(id)
            return candidate.first_name
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate name: {excpt}')
        return None

    def get_candidate_surname_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's surname by given id
        :param id: id of the candidate
        :return: candidate's surname or None if there is no such candidate
        """
        try:
            candidate = self.session.query(Users).get(id)
            return candidate.last_name
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate surname: {excpt}')
        return None

    def get_candidate_info_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's info instance by given id
        :param id: id of the candidate
        :return: candidate's info instances or None if there is no such candidate
        """
        try:
            candidate_info = self.session.query(CandidatesInfo).get(id)
            return candidate_info
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates info: {excpt}')
        return None

    def get_candidate_nationality_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's nationality by given id
        :param id: id of the candidate
        :return: candidate's nationality or None if there is no such candidate
        """
        try:
            candidate = self.session.query(CandidatesInfo).get(id)
            return candidate.nationality
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate nationality: {excpt}')
        return None

    def get_candidate_gender_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's gender by given id. Converts it to the male or female instead of boolean value.
        :param id: id of the candidate
        :return: candidate's gender or None if there is no such candidate
        """
        try:
            candidate = self.session.query(CandidatesInfo).get(id)
            gender = candidate.gender
            if gender == False:
                return ('Male')
            else:
                return ('Female')
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate gender: {excpt}')
        return None

    def get_candidate_age_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's date of birth and calculates age
        :param id: id of the candidate
        :return: candidate's age or None if there is no such candidate
        """
        try:
            candidate = self.session.query(CandidatesInfo).get(id)
            date_of_birth = candidate.date_of_birth
            today = date.today()
            return today.year - date_of_birth.year - (
                    (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate nationality: {excpt}')
        return None

    def get_candidate_email_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's email by given id
        :param id: id of the candidate
        :return: candidate's email or None if there is no such candidate
        """
        try:
            candidate = self.session.query(CandidatesInfo).get(id)
            return candidate.email
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate email: {excpt}')
        return None

    def get_candidate_skype_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's skype by given id
        :param id: id of the candidate
        :return: candidate's skype or None if there is no such candidate
        """
        try:
            candidate = self.session.query(CandidatesInfo).get(id)
            return candidate.skype
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate skype: {excpt}')
        return None

    def get_candidate_phone_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's phone by given id
        :param id: id of the candidate
        :return: candidate's phone or None if there is no such candidate
        """
        try:
            candidate = self.session.query(CandidatesInfo).get(id)
            return candidate.phone
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate nationality: {excpt}')
        return None

    def get_candidate_documents_by_id(self, id: int) -> Optional[Users]:
        """
        Get candidate's documents instance by given id
        :param id: id of the candidate
        :return: candidate's documents instances or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates documents: {excpt}')
        return None

    def get_candidate_cv_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's cv by given id
        :param id: id of the candidate
        :return: candidate's cv or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.cv
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates cv: {excpt}')
        return None

    def get_candidate_letter_of_recommendation_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's letter of recomendation by given id
        :param id: id of the candidate
        :return: candidate's letter of recommendation or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.letter_of_recomendation
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates letter of recomendation: {excpt}')
        return None

    def get_candidate_motivation_letter_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's motivation letter by given id
        :param id: id of the candidate
        :return: candidate's motivation letter or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.motivation_letter
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates motivation letter: {excpt}')
        return None

    def get_candidate_passport_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's passport by given id
        :param id: id of the candidate
        :return: candidate's passport or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.passport
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates passport: {excpt}')
        return None

    def get_candidate_photo_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's photo by given id
        :param id: id of the candidate
        :return: candidate's photo or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.photo
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates photo: {excpt}')
        return None

    def get_candidate_project_description_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's project description by given id
        :param id: id of the candidate
        :return: candidate's project description or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.project_description
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates project description: {excpt}')
        return None

    def get_candidate_transcript_by_id(self, id: int) -> Optional[Users]:
        """
        Get link to candidate's transcript by given id
        :param id: id of the candidate
        :return: candidate's transcript or None if there is no such candidate
        """
        try:
            candidate_documents = self.session.query(CandidatesDocuments).get(id)
            return candidate_documents.transcript
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidates transcript: {excpt}')
        return None

    def get_test(self, id: int) -> Optional[Tests]:
        """
        Takes test instance from the database by test id
        :param id: id of the test
        :return: test instance from the database. Or None if test was not found
        """
        try:
            test = self.session.query(Tests).get(id)
            return test
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get test: {excpt}')
        return None

    def get_question(self, id: int) -> Optional[Questions]:
        """
        Takes the question instance from the database by the question id
        :param id: id of the question
        :return: question instance from the database or none if there is no such question
        """
        try:
            queston = self.session.query(Questions).get(id)
            return queston
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get question: {excpt}')
        return None

    def get_qustions_test(self, question_id: int) -> Optional[QuestionsTests]:
        """
        Returns instance from the table that links questions and tests
        :param question_id: id of the question to search appropriate test
        :return: questions tests instance from the database
        """
        try:
            questions_tests = self.session.query(QuestionsTests).get(question_id)
            return questions_tests
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get question test link: {excpt}')
        return None

    # ------------
    # DELETE

    def delete_token(self, id: int) -> Optional[int]:
        """
        Deletes given token by id
        :param id: id of the given token to delete
        :return: True if token was delete successfully, False if token was not found, None in case of error
        """
        try:
            existing_token = self.session.query(RevokedToken).filter_by(id=id).first()
            if existing_token:
                self.session.delete(existing_token)
                self.session.commit()
                return True
            else:
                return False  # there is no such token

        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t delete revoked token: {excpt}')
        return None

    def delete_candidate(self, id: int) -> Optional[int]:
        """
        This function will delete all candidates data including candidate's info, tests passed by candidate and etc
        :param id: the id of the candidate
        :return: True if candidate was delete successfully, False if candidate was not found, None in case of error
        """
        try:
            existiing_candidate = self.session.query(Users).filter_by(id=id).first()
            if existiing_candidate:
                self.session.delete(existiing_candidate)
                self.session.commit()
                return True
            else:
                return False  # there is no such candidate

        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t delete candidate: {excpt}')
        return None

    def delete_candidates_documents(self, id: int) -> Optional[int]:
        """
        Deletes all candidates' documents by given candidate's id
        :param id: the id of the candidate
        :return: True if candidate's documents were deleted successfully, False if candidate_documents were not found, None in case of error
        """
        try:
            existiing_candidates_documents = self.session.query(CandidatesDocuments).filter_by(id=id).first()
            if existiing_candidates_documents:
                self.session.delete(existiing_candidates_documents)
                self.session.commit()
                return True
            else:
                return False  # there is no such candidates documents

        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t delete candidate documents: {excpt}')
        return None
