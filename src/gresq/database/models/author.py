from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func, text, and_
from sqlalchemy.sql import exists
from sqlalchemy.schema import Table
from sqlalchemy.dialects.postgresql import *


from gresq.database import Base, class_registry

sample_association_table = Table('sample_association', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('sample_name', Integer, ForeignKey('sample.id'))
)

class Author(Base):
    """[summary]
    
    Args:
        Base ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    __tablename__ = "author"

    id = Column(Integer, primary_key=True, info={"verbose_name": "ID"})

    first_name = Column(
        String(64), info={"verbose_name": "First Name", "required": False}
    )
    last_name = Column(
        String(64), info={"verbose_name": "Last Name", "required": False}
    )
    institution = Column(
        String(64), info={"verbose_name": "Institution", "required": False}
    )
    nanohub_userid = Column(
        Integer, info={"verbose_name": "Nanohub Submitter User ID"}
    )
    submitted_samples = relationship("Sample")
    authored_samples = relationship("Sample", secondary=sample_association_table, back_populates="authors")
    
    @hybrid_property
    def full_name_and_institution(self):
        return "%s, %s   (%s)" % (self.last_name, self.first_name, self.institution)
    
    

