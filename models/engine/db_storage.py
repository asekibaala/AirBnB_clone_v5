from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    """Defines the DBStorage engine for MySQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database engine."""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries all objects of a given class or all objects."""
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cls_name in [User, State, City, Amenity, Place, Review]:
                query = self.__session.query(cls_name).all()
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Adds an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads the database session."""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)