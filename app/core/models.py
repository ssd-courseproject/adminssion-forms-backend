from typing import Set, List, Optional, Tuple
from sqlalchemy import create_engine, Column, Date, Boolean, Text, BigInteger, ForeignKey, ForeignKeyConstraint, \
    UniqueConstraint, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class RevokedTokenModel(Base):
    __tablename__ = 'revoked_tokens'
    id = Column(BigInteger, primary_key=True)
    jti = Column(Text(120))


'''
    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
'''


class Candidate(Base):
    """
    Keeps the general info about candidates such as Name, Surname and id
    """
    __tablename__ = 'candidates'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)

    autorization = relationship('CandidatesAutorization', backref='candidate', uselist=False)  # one-to-one
    info = relationship('CandidatesInfo', backref='candidate', uselist=False)  # one-to-one
    status = relationship('CandidatesStatus', backref='candidate', uselist=False)  # one-to-one
    documents = relationship('CandidatesDocuments', backref='candidate', uselist=False)  # one-to-one


class CandidatesAutorization(Base):
    """
    Keeps data email and password for candidates' authorization
    """
    __tablename__ = 'candidates_autorization'
    __table_args__ = {'extend_existing': True}

    email = Column(Text, primary_key=True)
    id = Column(BigInteger, ForeignKey('candidates.id'), unique=True)  # one to one
    password = Column(Text)


class CandidatesInfo(Base):
    """
    Keeps info about each candidate such as nationality, gender, date of birth and email
    """
    __tablename__ = 'candidates_info'

    id = Column(BigInteger, ForeignKey('candidates.id'), primary_key=True)  # one-to-one
    nationality = Column(Text)
    gender = Column(Boolean)
    date_of_birth = Column(Date)
    subscription_email = Column(Text)
    skype = Column(Text)
    phone = Column(Text)


class CandidatesDocuments(Base):
    """
    Keeps link on candidate's documents
    """
    __tablename__ = 'candidates_documents'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey('candidates.id'), primary_key=True)  # one-to-one
    cv = Column(Text)
    letter_of_recomendation = Column(Text)
    motivation_letter = Column(Text)
    passport = Column(Text)
    photo = Column(Text)
    project_description = Column(Text)
    transcript = Column(Text)


class CandidatesStatus(Base):
    """
    Keeps info about candidate's status which is enum accepted/rejected/waiting_list
    """
    __tablename__ = 'candidates_info'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey('candidates.id'), primary_key=True)  # one-to-one
    status = Column(BigInteger)


class CandidatesTests(Base):
    """
    Keeps info about tests that were passed by candidate
    """
    __tablename__ = 'candidates_tests'
    __table_args__ = {'extend_existing': True}

    # composite primary key
    id = Column(BigInteger, ForeignKey('candidates.id'), primary_key=True)  # one-to-one
    question_id = Column(BigInteger, ForeignKey('questions.id'), primary_key=True)
    start_date = Column(Date, default=datetime.datetime.utcnow)
    end_date = Column(Date)
    answer = Column(Text)
    points = Column(BigInteger)


class Questions(Base):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, ForeignKey('questions_tests.question_id'), primary_key=True)
    question = Column(Text)
    # TODO: add more fields

    questions = relationship('QuestionsTests', backref='questions_tests', uselist=False)  # one-to-one


class QuestionsTests(Base):
    __tablename__ = 'questions_tests'
    __table_args__ = {'extend_existing': True}

    question_id = Column(BigInteger, ForeignKey('questions.id'), primary_key=True)
    test_id = Column(BigInteger, ForeignKey('tests.id'))


class Tests(Base):
    __tablename__ = 'tests'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    test_name = Column(Text)

    questions_tests = relationship('QuestionsTests', backref='questions_tests', uselist=False)  # one-to-one


class ORM:
    """
    Supports AddOrUpdate and Remove operations for all the non-associative tables
    Should automatically handle starting/finishing the session
    """

    def __init__(self):
        POSTGRES_ADDRESS = self.get_postgres_address('posgres', 'qwerty987', 'admissionDB', 'localhost', 5432)
        self.engine = create_engine(POSTGRES_ADDRESS, client_encoding='utf8')
        self.session = self._get_session()

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
    def add_candidate(self, first_name: str = None, last_name: str = None) -> Optional[int]:
        """
        Adds new candidate to the database
        """
        try:
            new_candidate = Candidate(first_name=first_name, last_name=last_name)
            self.session.add(new_candidate)
            self.session.commit()
            return new_candidate.id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add new candidate: {excpt}')
        return None

    def add_candidates_info(self, candidate_id, nationaity: str = None, gender: bool = False,
                            date_of_birth: Date = None,
                            subscription_email: str = None, skype: str = None, phone: str = None) -> Optional[int]:
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
        try:
            existing_candidates_autorization = self.session.query(CandidatesAutorization).filter_by(email=email).first()
            if not existing_candidates_autorization:
                candidate_autorization = CandidatesAutorization(email=email, id=id, password=password)
                self.session.add(candidate_autorization)
                self.session.commit()
                return candidate_autorization.email
            else:
                return existing_candidates_autorization
        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t add candidates autorization: {excpt}')
        return None

    def add_candidates_documents(self, id: int, cv: str = None, letter_of_recomendation: str = None,
                                 motivation_letter: str = None, passport: str = None, photo: str = None,
                                 project_description: str = None, transcript: str = None) -> Optional[int]:
        try:
            candidates_documents = CandidatesDocuments(id=id, cv=cv, letter_of_recomendation=letter_of_recomendation,
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

    def add_candidates_tests(self, candidate_id: int, question_id: int, start_date: Date, end_date: Date, answer: str,
                             points: str = None) -> Optional[int]:
        try:
            existing_candidates_tests = self.session.query(CandidatesTests).filter_by(candidate_id=id,
                                                                                      question_id=question_id).first()
            if not existing_candidates_tests:
                candidates_tests = CandidatesTests(id=candidate_id, question_id=question_id, answer=answer,
                                                   points=None)
                self.session.add(candidates_tests)
                self.session.commit()
                return candidates_tests.id
            else:
                # case of changing the answer
                existing_candidates_tests.answer = answer
                self.session.commit()
                return existing_candidates_tests.id
        except Exception as excpt:
            self.session.rollback()
        print(f'Couldn\'t add candidates test: {excpt}')
        return None
