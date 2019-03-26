from typing import Set, List, Optional, Tuple
from sqlalchemy import create_engine, Column, Date, Boolean, Text, BigInteger, ForeignKey, ForeignKeyConstraint, \
    UniqueConstraint, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session, scoped_session


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
