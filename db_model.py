from typing import Set, List, Optional, Tuple
from sqlalchemy import create_engine, Column, Date, Boolean, Text, BigInteger, ForeignKey, ForeignKeyConstraint, \
    UniqueConstraint, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
            print(f'Couldn\'t add new Person tuple: {excpt}')
        return None
