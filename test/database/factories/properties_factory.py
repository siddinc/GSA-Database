import factory

from grdb.database.v1_1_0.models import Properties
from grdb.database.v1_1_0.dal import dal

LIST_SIZES = [1, 2, 3, 4, 5, 6]


class PropertiesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Properties
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"

    experiment_id = 2

    average_thickness_of_growth = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    standard_deviation_of_growth = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    number_of_layers = factory.Faker("pyint", min_value=0, max_value=3, step=1)
    growth_coverage = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=100.0
    )
    domain_size = factory.Faker("pyfloat", min_value=0.0, max_value=10.0)
    shape = factory.Iterator(Properties.shape.info["choices"])