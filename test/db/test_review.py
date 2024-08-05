import unittest
from src.db.databasemanager import DatabaseManager
from typing import NoReturn, AnyStr
from src.db.review import Review
from src.db.kpi import KPI
from src.db.permitofficial import PermitOfficial
import datetime


class ReviewTest(unittest.TestCase):
    database_manager: DatabaseManager = None

    def test_add(self):
        import random
        try:
            ReviewTest.__create_database_manager()
            review_count = ReviewTest.database_manager.query_count(ReviewTest.id)
            kpi_count = ReviewTest.database_manager.query_count(KPI.id)
            print(f'Table Review has {review_count} and KPY has {kpi_count} entries prior insert')
            kpi_entry = KPI(
                helpfulness=random.randint(1, 5),
                consistency=random.randint(1, 5),
                responsiveness=random.randint(1, 5),
                cost=random.randint(0, 5))
            ReviewTest.database_manager.add(kpi_entry)

            officials_count = ReviewTest.database_manager.query_count(PermitOfficial.id)
            official_id = 1 if officials_count < 1 else officials_count-1
            official = ReviewTest.database_manager.query(
                DatabaseManager.q_permit_officials,
                PermitOfficial.id == official_id
            )

            user, comment = ReviewTest.__create_review()
            permit_idx = 0 if review_count < 0 else review_count
            review_entry = Review(
                date=datetime.datetime.now(),
                user_name=user,
                permit=f'AP-10{permit_idx}',
                comment=comment,
                kpi_id=kpi_count,
                permit_official_id=official_id
            )
            ReviewTest.database_manager.add(review_entry)
            new_review_count = ReviewTest.database_manager.query_count(ReviewTest.id)
            print(f'Table Review has {ReviewTest.id} entries after insert')
            self.assertEqual(new_review_count, review_count + 1)
        except Exception as e:
            self.assertTrue(False, {str(e)})

    @unittest.skip('Ignore')
    def test_delete(self):
        try:
            ReviewTest.__create_database_manager()
            count = ReviewTest.database_manager.query_count(Review.id)

            print(f'Table Review has {count} entries prior deletion')
            ReviewTest.database_manager.delete_entry(Review, count)
            new_count = ReviewTest.database_manager.query_count(Review.id)
            print(f'Table Review has {new_count} entries after deletion')
            self.assertEqual(new_count, count-1)
        except Exception as e:
            self.assertTrue(False, {str(e)})

    """ -----------------------  Supporting methods ----------------- """

    @staticmethod
    def __create_review() -> (AnyStr, AnyStr):
        import random

        names = ['Jake', 'Sherry', 'Bernard', 'Rob', 'Sunny', 'Ashley']
        name_index = random.randint(0, len(names)-1)
        comments = f'This is a comment from our friend {names[name_index]}'
        return names[name_index], comments

    @staticmethod
    def __create_database_manager() -> NoReturn:
        if ReviewTest.database_manager is None:
            user_name = 'pat_nicolas'
            password = DatabaseManager.default_password
            db_name = 'test_rating'
            ReviewTest.database_manager = DatabaseManager(user_name, password, db_name)


