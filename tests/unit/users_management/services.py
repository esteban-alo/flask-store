import unittest
from app.api.users_management.users.services import UserService


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_service = UserService()

    def test_something(self):
        self.assertEqual(self.user_service.get_user_data("Esteban"), "Esteban")


if __name__ == "__main__":
    unittest.main()
