import factory
import random

from gresq.database.models.user.user import User
from gresq.database.dal import dal

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"

    preparation_steps = factory.RelatedFactoryList(
        "test.database.factories.PreparationStepFactory", "recipe", size=1
    )