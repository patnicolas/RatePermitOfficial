import unittest
from src.db.databasemanager import DatabaseManager
from src.db.review import Review
from sqlalchemy.orm import Session
from src.db.kpi import KPI
from src.db.permitofficial import PermitOfficial
from typing import Any, NoReturn


class DatabaseManagerTest(unittest.TestCase):
    database_manager: DatabaseManager = None

    def test_init(self):
        DatabaseManagerTest.__create_database_manager()
        print(str(DatabaseManagerTest.database_manager))
        self.assertTrue(True)

    @unittest.skip('Ignore')
    def test_max_review(self):
        DatabaseManagerTest.__create_database_manager()
        field = Review.id
        count = DatabaseManagerTest.database_manager.query_count(field)
        print(f'Maximum index for Review table is {count}')

    @unittest.skip('Ignore')
    def test_delete_all(self):
        DatabaseManagerTest.__create_database_manager()
        DatabaseManagerTest.database_manager.delete_all()

    @unittest.skip('Ignore')
    def test_query_join(self):
        DatabaseManagerTest.__create_database_manager()


        def q1(session: Session) -> Any:
            return session.query(Review, PermitOfficial)

        def q2(session: Session) -> Any:
            return session.query(Review, KPI, PermitOfficial)

        results = DatabaseManagerTest.database_manager.query_join(
            DatabaseManager.q_reviews_kpi_permit_officials,
            Review.permit_official_id == PermitOfficial.id and Review.kpi_id == KPI.id)

        for result in results:
            review, kpi, permit_official = result
            average_kpi = (kpi.consistency + kpi.helpfulness + kpi.cost + kpi.responsiveness)*0.25
            output = f'{review.user_name} {review.comment} {review.date} {kpi.cost} {kpi.consistency} ' \
                     f'{kpi.helpfulness} {kpi.responsiveness} {average_kpi} {permit_official.last_name} ' \
                     f'{permit_official.title} {permit_official.city}'
            print(output)



    """ --------------------  Supporting methods ------------------ """

    @staticmethod
    def __get_random_id(field: Any) -> int:
        import random

        max_id = DatabaseManagerTest.database_manager.query_count(field)-1
        return random.randint(1, max_id)

    @staticmethod
    def __create_database_manager() -> NoReturn:
        if DatabaseManagerTest.database_manager is None:
            user_name = 'pat_nicolas'
            password = 'Yge_1908'
            db_name = 'test_rating'
            DatabaseManagerTest.database_manager = DatabaseManager(user_name, password, db_name)


if __name__ == '__main__':
    unittest.main()

