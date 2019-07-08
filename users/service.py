"""User Service module"""

from mongoengine import connect

from model import UserModel

class UserService():
    """User model service for injection"""

    def __init__(self):
        """Initializes the db connection"""
        self.connect_to_mongo()

    def connect_to_mongo(self):
        """Performs mongo connection"""
        self.is_connected_to_mongo = True
        connect('users_db', host='users_db')

    def ensure_mongo_conection(self):
        """Ensures the connection to mongo"""
        if not self.is_connected_to_mongo:
            self.connect_to_mongo()

    def create_new(self, *args, **kwargs):
        """Creates an empty user data object"""
        self.ensure_mongo_conection()
        return UserModel(*args, **kwargs)

    def find(self, *args, **kwargs):
        """Performs a query over the database and returns the first result"""
        return self.query(*args, **kwargs).first()

    def find_all(self, page, page_size, *args, **kwargs):
        """Performs a query over the database and returns all results"""
        results = []
        begin = page * page_size
        end = begin + page_size

        for user in self.query(*args, **kwargs)[begin:end]:
            results.append(user)

        return results

    def query(self, *args, **kwargs):
        """Performs a query over the database and returns a queryset"""
        self.ensure_mongo_conection()
        return UserModel.objects(*args, **kwargs)
