import factory

from grdb.database.v1_1_0.models import Substrate
from grdb.database.v1_1_0.dal import dal

class SubstrateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Substrate
        sqlalchemy_session = dal.Session()
        sqlalchemy_session_persistence = "commit"
    
    # MANY-TO-ONE: substrate->experiment
    experiments = factory.RelatedFactoryList(
        "test.database.factories.ExperimentFactory", "experiment", size=3
    )

    catalyst = factory.Iterator(Substrate.catalyst.info["choices"])
    thickness = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    diameter = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    length = factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )
    surface_area= factory.Faker(
        "pyfloat", positive=False, min_value=0.0, max_value=10.0
    )