from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Photo, User
from datetime import date

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
             picture='https://lh6.googleusercontent.com/-6UvqVKKRcnE/AAAAAAAAAAI/AAAAAAAAIu8/Xb7i_PfEOXc/photo.jpg')
session.add(user1)
session.commit()

# Photos for City&Architecture
category1 = Category(user_id=1, name="City & Architecture")
session.add(category1)
session.commit()

photo1 = Photo(user_id=1, name="Sunset Hancock", description="John Hancock Tower, Chicago caught at sunset on a cloudy day.",
                     dateTaken=date(2015,10,7), width="4906", height="6132", camera="D800", 
                     image="https://drscdn.500px.org/photo/124381695/m%3D900/657602e4ceb6922a67fae5305fea8f1e",
                     category=category1)
session.add(photo1)
session.commit()

photo2 = Photo(user_id=1, name="Shadow of the Sun", description="November sunrise over Chicago skyline, catching shadows falling off the buildings and the church.",
                     dateTaken=date(2015,11,2), width="7360", height="3680", camera="D800", 
                     image="https://drscdn.500px.org/photo/127741419/m%3D900/b73bb89a63c07ad64a9701a24469c05f",
                     category=category1)
session.add(photo2)
session.commit()

photo3 = Photo(user_id=1, name="Urban Life", description="Urban Living",
                     dateTaken=date(2015,8,24), width="2117", height="2646", camera="D800", 
                     image="https://drscdn.500px.org/photo/119428413/m%3D900/0bf4289d2c20e53ec1bacd9befaf0b06",
                     category=category1)
session.add(photo3)
session.commit()

photo4= Photo(user_id=1, name="Concrete & Steel", description="Beauty can come from many things including the coldness of concrete and steel.",
                     dateTaken=date(2015,8,23), width="7086", height="4729", camera="D800", 
                     image="https://drscdn.500px.org/photo/119316311/m%3D900/df51a89db77b7596db19c7f2c8547349",
                     category=category1)
session.add(photo4)
session.commit()

# Photos for Weather
category2 = Category(user_id=1, name="Weather")
session.add(category2)
session.commit()


photo1 = Photo(user_id=1, name="Disappearing City", description="Chicago being swallowed by fog during sunrise.",
                     dateTaken=date(2015,12,4), width="7360", height="3680", camera="D800", 
                     image="https://drscdn.500px.org/photo/131222839/m%3D900/06d783156014dc148b4f314aa39c47d8",
                     category=category2)
session.add(photo1)
session.commit()

photo2 = Photo(user_id=1, name="Ice Monsters", description="Huge ice formations along Lake Michigan.",
                     dateTaken=date(2015,2,26), width="7360", height="4912", camera="D800", 
                     image="https://drscdn.500px.org/photo/100224451/m%3D900/707417090237c4f810da7a2c474eae08",
                     category=category2)
session.add(photo2)
session.commit()

photo3 = Photo(user_id=1, name="Strike!", description="Chicago Storm",
                     dateTaken=date(2013,9,18), width="3281", height="2173", camera="D800", 
                     image="https://drscdn.500px.org/photo/46843664/m%3D900/154c5778c3471d28c8fb22cf1279829e",
                     category=category2)
session.add(photo3)
session.commit()

photo4= Photo(user_id=1, name="Navy Pier Chicago", description="Navy Pier behind the steam of Lake Michigan during the Polar Vortex over Chicago",
                     dateTaken=date(2014,1,7), width="7211", height="2669", camera="D800", 
                     image="https://drscdn.500px.org/photo/57334470/m%3D900/1a94f64242fe9c924cef2d29806c081d",
                     category=category2)
session.add(photo4)
session.commit()


# Photos for Black & White
category3 = Category(user_id=1, name="Black & White")
session.add(category3)
session.commit()


photo1 = Photo(user_id=1, name="Look Down", description="Chicago EL in winter.",
                     dateTaken=date(2015,2,11), width="4134", height="4134", camera="D800", 
                     image="https://drscdn.500px.org/photo/98642457/m%3D900/f3f62b51eca45d9324152e9bf8dabd51",
                     category=category3)
session.add(photo1)
session.commit()

photo2 = Photo(user_id=1, name="Cold Commute", description="Snow falls during winter commute.",
                     dateTaken=date(2015,1,7), width="5235", height="3494", camera="D800", 
                     image="https://drscdn.500px.org/photo/95627701/m%3D900/d3f650e5400f534b52f88a48efbb08ff",
                     category=category3)
session.add(photo2)
session.commit()

photo3 = Photo(user_id=1, name="Only You", description="Couple in love holding hands",
                     dateTaken=date(2014,7,25), width="7360", height="4912", camera="D800", 
                     image="https://drscdn.500px.org/photo/77696281/m%3D900/dc0281ac130654873cfa198096636f64",
                     category=category3)
session.add(photo3)
session.commit()

photo4= Photo(user_id=1, name="Park Bench", description="Sunday afternoon in Olive Park enjoying Chicago skyline",
                     dateTaken=date(2014,5,13), width="7360", height="4912", camera="D800", 
                     image="https://drscdn.500px.org/photo/70416921/m%3D900/dda577d2b72ab0787e324676805ea568",
                     category=category3)
session.add(photo4)
session.commit()

# Photos for Abstract
category4 = Category(user_id=1, name="Abstract")
session.add(category4)
session.commit()

photo1 = Photo(user_id=1, name="Umbrella & Orb", description="Paraigues i Orbe",
                     dateTaken=date(2015,12,30), width="3000", height="2524", camera="", 
                     image="https://drscdn.500px.org/photo/134078971/m%3D900/64af3c1f475b0f033a2ca3a434a0e723",
                     category=category4)
session.add(photo1)
session.commit()

# Photos for People
category5 = Category(user_id=1, name="People")
session.add(category5)
session.commit()

photo1 = Photo(user_id=1, name="Keine sonne die mir scheint", description="Model: Kseniya Voronovich | Ambient light | Minsk, Belarus.",
                     dateTaken=date(2015,12,30), width="1400", height="794", camera="", 
                     image="https://drscdn.500px.org/photo/134033395/m%3D900/bf8c80386099d26e4ebd3e24c32ed1c7",
                     category=category5)
session.add(photo1)
session.commit()

# Photos for Nature
category6 = Category(user_id=1, name="Nature")
session.add(category6)
session.commit()

photo1 = Photo(user_id=1, name="Yellow Warbler .....", description="This resident yellow warbler is one of the many highlights of this years travels",
                     dateTaken=date(2015,12,29), width="665", height="900", camera="", 
                     image="https://drscdn.500px.org/photo/134006773/m%3D900/deca405ed0aa1bf26e67517f63b78044",
                     category=category6)
session.add(photo1)
session.commit()

# Photos for Sport
category7 = Category(user_id=1, name="Sport")
session.add(category7)
session.commit()

photo1 = Photo(user_id=1, name="Race of Christmas in Jarama (Madrid)", description="",
                     dateTaken=date(2015,12,20), width="6132", height="4096", camera="", 
                     image="https://drscdn.500px.org/photo/134059963/m%3D900/76c154c159dd4547631497b681d2ab6c",
                     category=category7)
session.add(photo1)
session.commit()

# Photos for Animals
category8 = Category(user_id=1, name="Animals")
session.add(category8)
session.commit()

photo1 = Photo(user_id=1, name="Snow Leopard Portrait", description="Snow Leopard Portrait",
                     dateTaken=date(2015,12,25), width="6132", height="4096", camera="D4S", 
                     image="https://drscdn.500px.org/photo/134024085/m%3D900/83d909b932fc176bb72efa9934260656",
                     category=category8)
session.add(photo1)
session.commit()

print "added menu items!"
