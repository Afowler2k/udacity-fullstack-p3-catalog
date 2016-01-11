from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

from xml.etree.ElementTree import Element, SubElement, Comment

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    name = Column(String(80), nullable=False)
    email = Column(String(80))
    picture = Column(String(80))
    id = Column(Integer, primary_key=True)
    
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
    # Convert object to XML
    @property
    def serializeXML(self):
      """Return object in XML format"""
      category = Element('category')

      name = SubElement(category, 'name')
      name.text = self.name

      categoryId = SubElement(category, 'id')
      categoryId.text = str(self.id)

      return category

    # Convert JSON to Category
    @classmethod
    def JSON_decoder(cls, obj):
      return cls(name=obj['name'])

class Photo(Base):
    __tablename__ = 'photo'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    dateTaken = Column(Date, default=datetime.datetime.now())
    width = Column(Integer)
    height = Column(Integer)
    camera = Column(String(80))
    image = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'dateTaken'    : self.dateTaken.strftime("%Y-%m-%d"),
           'width'        : self.width,
           'height'       : self.height,
           'camera'       : self.camera,
           'image'        : self.image
       }

    # Convert object to XML
    @property
    def serializeXML(self):
      """Return object in XML format"""
      photo = Element('photo')

      name = SubElement(photo, 'name')
      name.text = self.name

      description = SubElement(photo, 'description')
      description.text = self.description

      photoId = SubElement(photo, 'id')
      photoId.text = str(self.id)

      dateTaken = SubElement(photo, 'dateTaken')
      dateTaken.text = self.dateTaken.strftime("%Y-%m-%d")

      width = SubElement(photo, 'width')
      width.text = str(self.width)

      height = SubElement(photo, 'height')
      height.text = str(self.height)

      camera = SubElement(photo, 'camera')
      camera.text = self.camera

      image = SubElement(photo, 'image')
      image.text = self.image

      return photo

    # Convert JSON to Photo
    @classmethod
    def JSON_decoder(cls, obj):
      return cls(name=obj['name'], 
                   description=obj['description'],
                   dateTaken=datetime.datetime.strptime(
                                    obj['dateTaken'],"%Y-%M-%d"),
                   width=int(obj['width']),
                   height=int(obj['height']),
                   camera=obj['camera'],
                   image=obj['image']
                   )

engine = create_engine('sqlite:///photogallery.db')
Base.metadata.create_all(engine)
