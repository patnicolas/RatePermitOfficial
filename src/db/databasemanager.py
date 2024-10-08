__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024  All rights reserved."


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from typing import AnyStr, NoReturn, List, Any, Callable, Self
from src.db.kpi import KPI
from src.db.user import User
from src.db.role import Role
from src.db.review import Review
from src.db.permitofficial import PermitOfficial
import logging
from src.web.reviewdata import ReviewData

""" Table types/classes used in the project """
TableType = Review | Role | PermitOfficial | User | KPI


def load_password() -> AnyStr:
    """
    Load and decrypted an encrypted password from a file
    :return: Decrypted password
    :rtype: Str
    """
    from src.util.keyencryption import KeyEncryption

    key_encryption = KeyEncryption()
    encrypted_password = b'gAAAAABmraC9-WtivAoSpMhPVIKP_Gam2GlisgzHp4hZHVRLQE09syHFUYPmVyiMvlMYsp14poJShCHutkfEdAzHoEWq7bNS3g=='
    return key_encryption.decrypt(encrypted_password)


class DatabaseManager(object):
    """ Default password decrypted from a file"""
    default_password: AnyStr = load_password()

    def __init__(self,
                 _user_name: AnyStr,
                 _password: AnyStr,
                 _db_name: AnyStr,
                 _host: AnyStr = 'localhost') -> None:
        """
        Constructor for the database manager that establish a SQL connection to a database and initiate
        a new session
        :param _user_name: User name to access database
        :type _user_name: str
        :param _password: Encrypted password
        :type _password: str
        :param _db_name: Name of database
        :type _db_name: str
        :param _host:host
        :type _host:str
        """
        from src.db import Base

        self.database_url = f'postgresql://{_user_name}:{_password}@{_host}/{_db_name}'
        self.engine = create_engine(self.database_url)
        self.session = self.create_session()
        """
        self.metadata = MetaData()
        Base.metadata.create_all(bind=self.engine)
        """

    @classmethod
    def build(cls) -> Self:
        """
        Ancillary constructor with database parameters loaded from a configuration file
        :return: Instance of database manager
        :rtype: DatabaseManager
        """
        from src.web.configparams import configuration_parameters

        _user_name = configuration_parameters['admin']
        _password = configuration_parameters['password']
        _db_name = configuration_parameters['db_name']
        _host = configuration_parameters['host']

        return cls(_user_name, _password, _db_name, _host)

        # return DatabaseManager.database_manager

    def create_session(self) -> Session:
        """
        Create a session for a given database engine
        :return: Database session
        :rtype: sqlalchemy.orm.Session
        """
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return Session()

    def __str__(self) -> AnyStr:
        return f'Database url: {self.database_url}'

    def close(self) -> NoReturn:
        """
        Close this session which is initiated in the constructor.
        create_session has to be called for subsequent calls
        """
        self.session.close()

    """
    @staticmethod
    def create_database_manager() -> NoReturn:
        if DatabaseManager.data_manager is None:
            user_name = 'pat_nicolas'
            password = DatabaseManager.default_password
            db_name = 'test_rating'
            DatabaseManager.data_manager = DatabaseManager(user_name, password, db_name)
        return DatabaseManager.data_manager
    """

    def add(self, _entry: TableType) -> TableType:
        """
        Add a new entry (or row) for a given table type
        :param _entry:
        :type _entry:
        :return:
        :rtype:
        """
        self.session.add(_entry)
        self.session.commit()
        self.session.refresh(_entry)
        return _entry

    """ ----------------------  Deletion ------------------------ """

    def delete_entry(self, table_type: TableType, entry_id: int) -> bool:
        """
        Delete a row or entry with id=entry_id from a given table
        :param table_type: Targeted table
        :type table_type: TableType
        :param entry_id: Row or entry id
        :type entry_id: int
        :return: True if successful, False otherwise
        :rtype: bool
        """
        try:
            _entry = self.session.query(table_type).filter(table_type.id==entry_id).first()
            if _entry:
                self.session.delete(_entry)
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            logging.error(f'Delete entry from table {table_type.__tablename__} with  {str(e)}')
            return False

    def delete_table(self, table: TableType) -> bool:
        """
        Delete or drop an entire table
        :param table: Targeted table
        :type table: TableType
        :return: True if successful, False otherwise
        :rtype: bool
        """
        try:
            table.__table__.drop(self.engine)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(f'Delete table: {table.__tablename__} with {str(e)}')
            return False

    def delete_all(self):
        """
        Delete all the table created from the constructor
        """
        from src.db import Base
        Base.metadata.drop_all(bind=self.engine)

    """ ----------------------  Queries ----------------------------- """

    def query_count(self, col_name: Any) -> int:
        """
        Query the number of rows for a given field
        :param col_name: Field of any give table
        :type col_name: Any
        :return: number of rows after query
        :rtype: int
        """
        try:
            return self.session.query(col_name).count()
        except Exception as e:
            logging.error(f'Query max index with {str(e)}')
            return -1

    def query(self, q: Callable[[Session], Any], condition: Any = None) -> Any:
        """
        Query a set of fields
        :param q: Function that specify the field to extract given the current session
        :type q: Callable
        :param condition: Where SQL condition as a boolean
        :type condition: Any
        :return: Result of query
        :rtype: Any
        """
        try:
            q_res = q(self.session)
            result = q_res.filter(condition).all() if condition is not None else q_res.all()
            return result
        except Exception as e:
            logging.error(f'Query fields with {str(e)}')
            return None

    def query_all(self, table_type: TableType) -> Any:
        """
        Query all the rows from a given table
        :param table_type: Targeted table
        :type table_type: TableType
        :return: Result of the query
        :rtype: Any
        """
        try:
            return self.session.query(table_type).all()
        except Exception as e:
            logging.error(f'Query fields with {str(e)}')
            return None

    def query_join(self, q: Callable[[Session], Any], condition: Any) -> Any:
        try:
            q_res = q(self.session)
            return q_res.filter(condition).all()
        except Exception as e:
            logging.error(f'Query join with {str(e)}')
            return None


    def add_review(self, review_data: ReviewData):
        import datetime

        logging.info(f'Initialize database {self.__str__()}')
        kpi_entry = KPI(
            helpfulness=review_data.helpfulness,
            consistency=review_data.consistency,
            responsiveness=review_data.responsiveness,
            cost=review_data.cost)
        kpi_entry_resp = self.add(kpi_entry)
        kpi_id = kpi_entry_resp.id

        official_ids = self.query(
            DatabaseManager.q_permit_official_id,
            PermitOfficial.last_name == review_data.permitofficial
        )
        official_id = official_ids[0][0]
        review_entry = Review(
            date=datetime.datetime.now(),
            user_name='Patrick',
            permit=review_data.permit,
            comment=review_data.comment,
            kpi_id=kpi_id,
            permit_official_id=official_id
        )
        self.add(review_entry)

    """ ----------------------   Query stubs --------------------- """

    @staticmethod
    def q_permit_officials(session: Session) -> Any:
        """
        Default query for all the relevant fields of permit officials table
        :param session: Current database session
        :type session: sqlalchemy.orm.Session
        :return: Result of the query
        :rtype: Any
        """
        return session.query(
            PermitOfficial.id,
            PermitOfficial.last_name,
            PermitOfficial.title,
            PermitOfficial.department,
            PermitOfficial.city)

    @staticmethod
    def q_permit_official_id(session: Session) -> int:
        """
        Default query for all the relevant fields of permit officials table
        :param session: Current database session
        :type session: sqlalchemy.orm.Session
        :return: Result of the query
        :rtype: Any
        """
        return DatabaseManager.q_permit_officials(session).id


    @staticmethod
    def q_reviews_kpi_permit_officials(session: Session) -> Any:
        """
        Default join query for Review, KPI and PermitOfficials
        :param session: Current session
        :type session: sqlalchemy.orm.Session
        :return: Result of the query
        :rtype: Any
        """
        return session.query(Review, KPI, PermitOfficial)

    @staticmethod
    def q_roles(session: Session) -> Any:
        return session.query(Role)

    @staticmethod
    def q_users(session: Session) -> Any:
        return session.query(User)

    @staticmethod
    def q_reviews(session: Session) -> Any:
        return session.query(Review)

    @staticmethod
    def q_reviews_profile(session: Session) -> Any:
        from sqlalchemy import func
        res = session.query(
            Review.date,
            func.count(Review.id).label('review_count')
        ).group_by(Review.date).order_by(Review.date)
        return res

    @staticmethod
    def q_permit_official_metrics(session: Session) -> Any:
        from sqlalchemy import func
        res = session.query(
            Review.permit_official_id,
            func.avg(Review.helpfulness).label('avg_helpfulness'),
            func.avg(Review.consistency).label('avg_consistency'),
            func.avg(Review.responsiveness).label('avg_responsiveness'),
            func.avg(Review.cost).label('avg_cost')
        ).group_by(Review.permit_official_id)
        return res

