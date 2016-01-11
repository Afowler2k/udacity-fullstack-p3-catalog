from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Photo, User
from datetime import date
import json


engine = create_engine('sqlite:///photogallery.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
user1 = User(name="Andy Fowler", email="andyfowler@gmail.com",
             picture='https://lh6.googleusercontent.com/-6UvqVKKRcnE/AAAAAAAAAAI/AAAAAAAAIu8/Xb7i_PfEOXc/photo.jpg')  # noqa
session.add(user1)
session.commit()

# load the JSON data file to populate the database
catalog = json.loads(open('photoCatalog.json', 'r').read())
for category in catalog['categories']:
       newCategory = Category.JSON_decoder(category)
       newCategory.user = user1
       session.add(newCategory)
       session.commit()

       for photo in category['Photos']:
              newPhoto = Photo.JSON_decoder(photo)
              newPhoto.user = user1
              newPhoto.category = newCategory
              session.add(newPhoto)
              session.commit()

print "added menu items!"
