from typing import Set, List, Optional, Tuple
from sqlalchemy import create_engine, Column, Date, Boolean, Text, BigInteger, ForeignKey, ForeignKeyConstraint, \
    UniqueConstraint, Numeric, Enum
from sqlalchemy.orm import relationship, sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import date

Base = declarative_base()


class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    jti = Column(Text(120))
    date = Column(Date)


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

    autorization = relationship('CandidatesAutorization', cascade="all,delete", backref='candidate',
                                uselist=False)  # one-to-one
    info = relationship('CandidatesInfo', cascade="all,delete", backref='candidate', uselist=False)  # one-to-one
    status = relationship('CandidatesStatus', cascade="all,delete", backref='candidate', uselist=False)  # one-to-one
    documents = relationship('CandidatesDocuments', cascade="all,delete", backref='candidate',
                             uselist=False)  # one-to-one
    tests = relationship('CandidatesTests', cascade="all,delete", backref='candidate', uselist=False)  # one-to-one


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
    __table_args__ = {'extend_existing': True}

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
    question_type = Column(BigInteger)
    answer = Column(Text)
    manually_grading = Column(Boolean, default=False)
    points = Column(BigInteger)

    questions = relationship('QuestionsTests', cascade="all,delete", backref='questions_tests',
                             uselist=False)  # one-to-one


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

    questions_tests = relationship('QuestionsTests', cascade="all,delete", backref='questions_tests',
                                   uselist=False)  # one-to-one


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

    def add_token(self, id: str, jti: str) -> Optional[int]:
        try:
            new_token = RevokedToken(id=id, jti=jti, date=datetime.utcnow)
            self.session.add(new_token)
            self.session.commit()
            return new_token.id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add new token: {excpt}')
        return None

    # ------------
    # GET
    def get_candidate_by_id(self, id: int) -> Optional[Candidate]:
        """
        Get candidate's instance by given id
        :param id: id of the candidate
        :return: candidate's instances or None if there is no such candidate
        """
        try:
            candidate = self.session.query(Candidate).get(id)
            return candidate
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate: {excpt}')
        return None

    def get_candidate_name_by_id(self, id: int) -> Optional[Candidate]:
        """
        Get candidate's name by given id
        :param id: id of the candidate
        :return: candidate's name or None if there is no such candidate
        """
        try:
            candidate = self.session.query(Candidate).get(id)
            return candidate.first_name
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate name: {excpt}')
        return None

    def get_candidate_surname_by_id(self, id: int) -> Optional[Candidate]:
        """
        Get candidate's surname by given id
        :param id: id of the candidate
        :return: candidate's surname or None if there is no such candidate
        """
        try:
            candidate = self.session.query(Candidate).get(id)
            return candidate.last_name
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get candidate surname: {excpt}')
        return None

    def get_candidate_info_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_nationality_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_gender_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_age_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_email_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_skype_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_phone_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_documents_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_cv_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_letter_of_recommendation_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_motivation_letter_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_passport_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_photo_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_project_description_by_id(self, id: int) -> Optional[Candidate]:
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

    def get_candidate_transcript_by_id(self, id: int) -> Optional[Candidate]:
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
            existiing_candidate = self.session.query(Candidate).filter_by(id=id).first()
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
