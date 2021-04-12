#!/usr/bin/env python3

from datetime import datetime, timedelta

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'Employee<id={self.id},name={self.name}>'


class PermanentRelationship(Base):
    __tablename__ = 'permanent_relationship'

    superior_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    inferior_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    department = Column(String)

    superior = relationship(
        Employee,
        backref=backref('perm_superiors'),
        foreign_keys=[superior_id])
    inferior = relationship(
        Employee,
        backref=backref('perm_inferiors'),
        foreign_keys=[inferior_id])

    def __repr__(self):
        return f'PermanentRelationship<superior_id={self.superior_id},' + \
            f'superior_id={self.superior_id},' + \
            f'inferior_id={self.inferior_id},' + \
            f'department={self.department}>'


class TemporaryRelationship(Base):
    __tablename__ = 'temporary_relationship'

    superior_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    inferior_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    setting = Column(String)
    starting = Column(DateTime)
    ending = Column(DateTime)

    superior = relationship(
        Employee,
        backref=backref('temp_superiors'),
        foreign_keys=[superior_id])
    inferior = relationship(
        Employee,
        backref=backref('temp_inferiors'),
        foreign_keys=[inferior_id])

    def __repr__(self):
        return f'PermanentRelationship<superior_id={self.superior_id},' + \
            f'superior_id={self.superior_id},' + \
            f'inferior_id={self.inferior_id},' + \
            f'setting={self.setting}' + \
            f'starting={self.starting},' + \
            f'ending={self.ending}>'


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    dilbert = Employee(name='Dilbert')
    ashok = Employee(name='Ashok')
    boss = Employee(name='Pointy-Haired Boss')

    session.add(dilbert)
    session.add(ashok)
    session.add(boss)
    session.flush()

    leadership = PermanentRelationship(
        superior=boss,
        inferior=dilbert,
        department='Engineering'
    )
    coaching = TemporaryRelationship(
        superior=dilbert,
        inferior=ashok,
        setting='Trainee Programme',
        starting=datetime.utcnow(),
        ending=datetime.utcnow() + timedelta(days=365)
    )

    session.add(leadership)
    session.add(coaching)

    for employee in session.query(Employee):
        print(
            employee,
            employee.perm_superiors,
            employee.perm_inferiors,
            employee.temp_superiors,
            employee.temp_inferiors)
