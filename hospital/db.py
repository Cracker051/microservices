import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()
database = databases.Database("mysql://root:87dima87@localhost:3306/new_hospital")
