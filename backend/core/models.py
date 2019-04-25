from datetime import datetime
from typing import List, Optional

from flask_jwt_extended import decode_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Boolean, Text, BigInteger, ForeignKey, Numeric, ARRAY, Integer, String, DateTime
from sqlalchemy.orm import relationship

from backend.core.enums import UsersRole, CandidateStatus, TokenType
from backend.helpers import _epoch_utc_to_datetime
from server import application

db = application.db


class TokenBlacklist(db.Model):
    """
    Storage of the token required for authentication
    """
    __tablename__ = 'token_blacklist'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    jti = Column(String(36), index=True, unique=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    expires = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    token_type = Column(Text, nullable=False)
    user_id = Column(BigInteger, index=True, nullable=False)


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


class Tests(db.Model):
    """
    All actual and archived tests in the system
    """
    __tablename__ = 'tests'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    test_name = Column(Text)
    max_time = Column(Integer)
    archived = Column(Boolean)

    questions_tests = relationship('QuestionsTests', cascade="all,delete", backref='tests',
                                   uselist=True)  # one-to-one
    # questions = relationship('Questions', cascade="all,delete", backref='questions_tests', # todo: is required?
    # uselist=False)  # one-to-one


class TestsSubmissions(db.Model):
    """
    Keeps data about tests that were submitted or started by a candidate
    """
    __tablename__ = 'candidates_submissions'
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True)
    candidate_id = Column(BigInteger, ForeignKey(Users.id))
    test_id = Column(Integer, ForeignKey(Tests.id))
    time_start = Column(Date, default=datetime.utcnow)
    time_end = Column(Date)
    submitted = Column(Boolean)
    graded_by = (BigInteger, ForeignKey(Users.id))

    answers = relationship('CandidatesAnswers', cascade="all,delete", backref='questions_tests',
                           uselist=True)


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

    def __init__(self, db_instance: SQLAlchemy):
        self.session = db_instance.session

    # ------------
    # SESSION
    # def get_postgres_address(user, password, db, host='localhost', port=5432):
    #     """Returns a url to connect with PostgreSQL"""
    #
    #     # We connect with the help of the PostgreSQL URL
    #     url = 'postgresql://{}:{}@{}:{}/{}'
    #     url = url.format(user, password, host, port, db)
    #     return url
    #
    # def _get_session(self) -> Optional[Session]:
    #     """Connects to database, and returns Session"""
    #     try:
    #         Session = scoped_session(sessionmaker(bind=self.engine))
    #         self.session = Session()
    #         return self.session
    #     except Exception as excpt:
    #         print(f'Can\'t connect to the database: {excpt}')
    #
    # def open_session(self):
    #     """Opens session"""
    #     if not self.session:
    #         self.session = self._get_session()
    #     else:
    #         print(f'Session for {self.engine} is already open')
    #
    # def close_session(self):
    #     """Closes session"""
    #     self.session.commit()
    #     self.session.close()
    #     self.session = None

    # ------------
    # ADD
    def add_user(self, first_name: str = None, last_name: str = None,
                 role: int = UsersRole.CANDIDATE) -> Optional[Users]:
        """
        Adds new candidate to the database
        """
        if isinstance(role, UsersRole):
            role = role.value

        try:
            new_candidate = Users(first_name=first_name, last_name=last_name, role=role)
            self.session.add(new_candidate)
            self.session.commit()

            return new_candidate
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add new candidate: {excpt}')

        return None

    def add_token(self, token: str, token_type: str, user_id: int, created: Date = None,
                  expires: Date = None, revoked: bool = False) -> Optional[int]:
        if isinstance(token_type, TokenType):
            token_type = token_type.value

        if len(token) > 36:
            decoded_token = decode_token(token)
            token = decoded_token['jti']
            if not expires:
                expires = _epoch_utc_to_datetime(decoded_token['exp'])

        try:
            new_token = TokenBlacklist(jti=token, date=created, expires=expires, token_type=token_type,
                                       user_id=user_id, revoked=revoked)
            self.session.add(new_token)
            self.session.commit()

            return new_token
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add new token: {excpt}')

        return None

    def add_candidates_info(self, candidate_id: int,
                            nationality: str = None, gender: bool = False,
                            date_of_birth: Date = None) -> Optional[CandidatesInfo]:
        """
        Adds all necessary candidate's info
        :param candidate_id: id of the given candidate
        :param nationality: nationality
        :param gender: boolean value. False for male and true for female
        :param date_of_birth: datetime
        :return: id of the given candidate or None in case of error
        """
        try:
            candidates_info = CandidatesInfo(id=candidate_id, nationaity=nationality,
                                             gender=gender, date_of_birth=date_of_birth)
            self.session.add(candidates_info)
            self.session.commit()

            return candidates_info
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add candidates info: {excpt}')

        return None

    def add_candidates_status(self, candidate_id: int,
                              status: int = CandidateStatus.PENDING,
                              admission_date: Date = None) -> Optional[CandidatesStatus]:
        try:
            candidates_status = CandidatesStatus(candidate_id=candidate_id, status=status,
                                                 admission_date=admission_date)
            self.session.add(candidates_status)
            self.session.commit()

            return candidates_status
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add candidates status: {excpt}')

        return None

    def add_candidates_authorization(self, email: str, u_id: int, password: str) -> Optional[int]:
        """
        Fill in all necessary fields for autorization
        :param email: candidates's email
        :param u_id: candidate's id
        :param password: candidates's password
        :return: new or existing autorization instance or None in case of error
        """
        try:
            existing_candidates_autorization = self.session.query(UsersAutorization).filter_by(email=email).first()
            if not existing_candidates_autorization:
                candidate_autorization = UsersAutorization(email=email, id=u_id, password=password)
                self.session.add(candidate_autorization)
                self.session.commit()
                return candidate_autorization
            else:
                return existing_candidates_autorization
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add candidates autorization: {excpt}')
        return None

    def add_candidates_documents(self, u_id: int,
                                 passport: str = None, photo: str = None,
                                 project_description: str = None,
                                 transcript: str = None) -> Optional[CandidatesDocuments]:
        """
        Add all necessary candidates documents (links to the files)
        :param u_id: candidate's id
        :param passport: link to the scan of the passport
        :param photo: link to the photo of given candidate
        :param project_description: link to the project description
        :param transcript: link to the transcript
        :return: id of the given candidate or None in case of error
        """
        try:
            candidates_documents = CandidatesDocuments(id=u_id, passport=passport,
                                                       photo=photo, project_description=project_description,
                                                       transcript=transcript)
            self.session.add(candidates_documents)
            self.session.commit()

            return candidates_documents
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add candidates documents: {excpt}')

        return None

    # tests adding
    def update_question(self, question: str, question_type: int, answer: [str],
                        manually_grading: bool, points: float,
                        test_id: int, question_id: int) -> Optional[int]:
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

            new_question = self.session.query(Questions) \
                .filter(Questions.id == question_id) \
                .update({'question': question, 'question_type': question_type, 'answer': answer,
                         'manually_grading': manually_grading,
                         'points': points, 'test_id': test_id, })
            self.session.flush()
            return new_question.id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add question: {excpt}')
        return None

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
            self.session.add(new_question)
            self.session.commit()
            new_questions_tests = QuestionsTests(question_id=new_question.id, test_id=test_id)
            self.session.add(new_questions_tests)
            self.session.commit()
            return new_question.id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add question: {excpt}')
        return None

    def add_answer(self, submission_id: int, question_id: int, answer: str) -> Optional[int]:
        try:
            new_answer = CandidatesAnswers(submission_id=submission_id, question_id=question_id, answer=answer)
            self.session.add(new_answer)
            self.session.commit()
            return new_answer.id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add test: {excpt}')
        return None

    def get_answers(self, submission_id) -> Optional[List[CandidatesAnswers]]:
        try:
            return self.session.query(CandidatesAnswers) \
                .filter(CandidatesAnswers.submission_id == submission_id).all()

        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get tests: {excpt}')

        return None

    def is_answer_exists(self, submission_id, question_id) -> Optional[bool]:
        try:
            answer = self.session.query(CandidatesAnswers) \
                .filter(CandidatesAnswers.submission_id == submission_id) \
                .filter(CandidatesAnswers.question_id == question_id).one()
            if answer is not None:
                return True
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get tests: {excpt}')

        return False

    def update_answer(self, submission_id: int, question_id: int,
                      answer: str, grade: int, comments: str) -> Optional[int]:
        try:
            self.session.query(CandidatesAnswers) \
                .filter(CandidatesAnswers.submission_id == submission_id).filter(
                CandidatesAnswers.question_id == question_id) \
                .update({'answer': answer, 'grade': grade, 'comments': comments})
            self.session.flush()
            self.session.commit()
            return submission_id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t change test: {excpt}')
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

    def init_submission(self, candidate_id: BigInteger, test_id: BigInteger):
        try:
            new_submission = TestsSubmissions(candidate_id=candidate_id,
                                              time_start=datetime.utcnow(), submitted=False,
                                              test_id=test_id)

            self.session.add(new_submission)
            self.session.commit()

            return new_submission
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add test: {excpt}')

        return None

    def update_submission(self, sub_id: int, submitted: bool, graded_by: int) -> Optional[int]:
        try:
            self.session.query(TestsSubmissions) \
                .filter(TestsSubmissions.id == sub_id) \
                .update({'submitted': submitted, 'graded_by': graded_by})
            self.session.flush()
            self.session.commit()
            return sub_id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t change test: {excpt}')
        return None

    def finish_submission(self, submission_id: int):
        try:
            self.session.query(TestsSubmissions) \
                .filter(TestsSubmissions.id == submission_id) \
                .update({'time_end': datetime.utcnow(), 'submitted': True})
            self.session.flush()
            self.session.commit()
            return submission_id
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t add test: {excpt}')

        return None

    # ------------
    # PUT
    def update_test(self, test_id: int, test_name: str, max_time: int, archived: bool = False) -> Optional[int]:
        try:
            self.session.query(Tests) \
                .filter(Tests.id == test_id) \
                .update({'test_name': test_name, 'max_time': max_time, 'archived': archived})
            self.session.flush()
            self.session.commit()

            return test_id
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not change test: {excpt}')

        return None

    def delete_test(self, test_id) -> Optional[bool]:
        try:
            existing_test = self.session.query(Tests).filter(Tests.id == test_id).first()
            if existing_test:
                self.session.delete(existing_test)
                self.session.commit()
                return True
            else:
                return False
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t delete test: {excpt}')

        return None

    def get_user(self, u_id: int) -> Optional[Users]:
        """
        Get user's instance by given id
        :param u_id: id of the user
        :return: user's instances or None if there is no such candidate
        """
        try:
            user = self.session.query(Users).get(u_id)

            return user
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not get user: {excpt}')

        return None

    def get_document(self, doc_id: int) -> Optional[Users]:
        """
        Get user's instance by given id
        :param u_id: id of the user
        :return: user's instances or None if there is no such candidate
        """
        try:
            doc = self.session.query(CandidatesDocuments).get(doc_id)

            return doc
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not get doc: {excpt}')

        return None

    def get_info(self, id: int) -> Optional[Users]:
        """
        Get user's instance by given id
        :param u_id: id of the user
        :return: user's instances or None if there is no such candidate
        """
        try:
            info = self.session.query(CandidatesInfo).get(id)

            return info
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not get uinfo: {excpt}')

        return None

    def get_status(self, id: int) -> Optional[Users]:
        """
        Get user's instance by given id
        :param u_id: id of the user
        :return: user's instances or None if there is no such candidate
        """
        try:
            status = self.session.query(CandidatesStatus).get(id)

            return status
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not get status: {excpt}')

        return None

    def get_user_auth_by_email(self, email: str) -> Optional[UsersAutorization]:
        """
        :param email: email of the user
        :return: user auth instance or None if there is no such candidate
        """
        try:
            user_auth = self.session.query(UsersAutorization).filter(UsersAutorization.email == email).first()

            return user_auth
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get user: {excpt}')

        return None

    def get_token_by_jti(self, jti) -> Optional[TokenBlacklist]:
        """
        Get token's instance by given id
        :param jti: id of the token
        :return: token's instances or None if there is no such token
        """
        try:
            token = self.session.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first()

            return token
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get token: {excpt}')

        return None

    def revoke_token_by_jti(self, jti: str) -> Optional[bool]:
        try:
            res = self.session.query(TokenBlacklist).filter_by(jti=jti).update({'revoked': True})
            self.session.flush()
            self.session.commit()

            return res
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get token: {excpt}')

            return None

    def get_test(self, t_id: int) -> Optional[Tests]:
        """
        Takes test instance from the database by test id
        :param t_id: id of the test
        :return: test instance from the database. Or None if test was not found
        """
        try:
            test = self.session.query(Tests).get(t_id)
            return test
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not get test: {excpt}')
        return None

    def get_tests(self) -> Optional[List[Tests]]:
        """
        Takes all tests instances from the database
        :return: all test instances from the database.
        """
        try:
            tests = self.session.query(Tests).filter(Tests.archived == 'false').all()
            return tests
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get tests: {excpt}')
        return None

    def get_submission(self, sub_id) -> Optional[List[TestsSubmissions]]:
        """
        Takes all tests instances from the database
        :return: all test instances from the database.
        """
        try:
            submission = self.session.query(TestsSubmissions).get(sub_id)
            return submission
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get tests: {excpt}')
        return None

    def get_submissions(self, test_id) -> Optional[List[TestsSubmissions]]:
        """
        Takes all tests instances from the database
        :return: all test instances from the database.
        """
        try:
            submissions = self.session.query(TestsSubmissions).filter(TestsSubmissions.test_id == test_id).all()
            return submissions
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get tests: {excpt}')
        return None

    def get_question(self, q_id: int) -> Optional[Questions]:
        """
        Takes the question instance from the database by the question id
        :param q_id: id of the question
        :return: question instance from the database or none if there is no such question
        """
        try:
            queston = self.session.query(Questions).get(q_id)

            return queston
        except Exception as excpt:
            self.session.rollback()
            print(f'Could not get question: {excpt}')

        return None

    def get_questions_test(self, question_id: int) -> Optional[QuestionsTests]:
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

    def delete_token(self, tid: int) -> Optional[int]:
        """
        Deletes given token by id
        :param tid: id of the given token to delete
        :return:
            True if token was delete successfully,
            False if token was not found,
            None in case of error
        """
        try:
            return self._remove_record(TokenBlacklist, tid)
        except Exception as excpt:
            print(f'Could not delete token: {excpt}')

            return None

    def delete_candidate(self, uid: int) -> Optional[int]:
        """
        This function will delete all candidates data including candidate's info, tests passed by candidate and etc
        :param uid: the id of the candidate
        :return:
            True if candidate was delete successfully,
            False if candidate was not found,
            None in case of error
        """
        try:
            return self._remove_record(Users, uid)
        except Exception as excpt:
            print(f'Could not delete candidate: {excpt}')

            return None

    def delete_candidates_documents(self, uid: int) -> Optional[bool]:
        """
        Deletes all candidates' documents by given candidate's id
        :param uid: the id of the candidate
        :return:
            True if candidate's documents were deleted successfully,
            False if candidate_documents were not found,
            None in case of error
        """
        try:
            return self._remove_record(CandidatesDocuments, uid)
        except Exception as excpt:
            print(f'Could not delete candidate documents: {excpt}')

            return None

    def get_users(self, page_num: int, num_of_users: int) -> Optional[List[Users]]:
        try:
            return self.session.query(Users).paginate(page_num, num_of_users, False).items
        except Exception as excpt:
            self.session.rollback()
            print(f'Couldn\'t get users: {excpt}')

        return None

    def _remove_record(self, model, row_id) -> bool:
        """
        Deletes row for given model
        :param model
        :param row_id
        :return:
        """
        try:
            model = self.session.query(model).filter_by(id=row_id).first()
            if model:
                self.session.delete(model)
                self.session.commit()

                return True
            else:
                return False

        except Exception:
            self.session.rollback()

            raise
