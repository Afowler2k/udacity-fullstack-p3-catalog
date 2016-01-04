from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Photo, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from datetime import date, datetime
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
from flask.ext.seasurf import SeaSurf

# enable CSRF protection in this app
app = Flask(__name__)
csrf = SeaSurf(app)

# load the secrets file for Google OAuth2 authentication to this application
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Photo Gallery Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///photogallery.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession() 


# Create route for the login page then
# create an anti-forgery state token, a random string of 32 chars of uppercase and digits
# store it in the state data of login_session
# render the login page and pass the state string to use when authenticating against the OAuth servers
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# server side google sign in implementation
@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
     
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    
    flash("you are now logged in as %s" % login_session['username'])
    
    return output


# Handle Google logout
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# server side facebook sign in implementation
@csrf.exempt
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

# Handle Facebook logout
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider and redirect to main page
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))

# Show all categories, if not logged in, only show the public page otherwise show the page with CRUD functionality
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if  'username' not in login_session:
      return render_template('publiccategories.html', categories=categories)
    else:
      return render_template('categories.html', categories=categories)

# Create a new category, and flash a message that it was created
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
      return redirect('login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])

        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
      return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)

# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
      return redirect('login')
 
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
      return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to delete.';}</script><body onload='myFunction()'' />"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)

# Show photos for category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/photos/')
def showPhotos(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    photos = session.query(Photo).filter_by(category_id=category_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
      return render_template('publicPhotos.html', photos = photos, category=category, creator=creator)
    else:
      return render_template('photos.html', photos=photos, category=category, creator=creator)

# Create a new photo
@app.route('/category/<int:category_id>/photo/new/', methods=['GET', 'POST'])
def newPhoto(category_id):
    if 'username' not in login_session:
      return redirect('login')
 
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        # use default date of today if none entered
        dateTaken = request.form.get('dateTaken', "");
        if dateTaken == "":
            dateTaken = datetime.now()
        else:
            dateTaken = datetime.strptime(dateTaken, "%Y-%M-%d")

        # create new photo with default values if any are missing
        newPhoto = Photo(name=request.form.get('name', ""), 
                         description=request.form.get('description', ""), 
                         dateTaken=dateTaken,
                         width=request.form.get('width', 0, type=int), 
                         height=request.form.get('height', 0, type=int), 
                         camera=request.form.get('camera', ""), 
                         image=request.form.get('image', ""), 
                         category_id=category_id,
                         user_id=category.user_id)
        session.add(newPhoto)
        session.commit()
        flash('New Photo %s Successfully Created' % (newPhoto.name))
        return redirect(url_for('showPhotos', category_id=category_id))
    else:
        return render_template('newphoto.html', category_id=category_id)

# Edit a photo
@app.route('/category/<int:category_id>/photo/<int:photo_id>/edit', methods=['GET', 'POST'])
def editPhoto(category_id, photo_id):
    if 'username' not in login_session:
      return redirect('login')

    editedPhoto = session.query(Photo).filter_by(id=photo_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form.has_key('name'):
            editedPhoto.name = request.form['name']
        if request.form.has_key('description'):
            editedPhoto.description = request.form['description']
        # convert the date string from form to Python date object
        if request.form.has_key('dateTaken'):
            editedPhoto.dateTaken = datetime.strptime(request.form['dateTaken'], "%Y-%M-%d")
        if request.form.has_key('width'):
            editedPhoto.width = request.form['width']
        if request.form.has_key('height'):
            editedPhoto.height = request.form['height']
        if request.form.has_key('camera'):
            editedPhoto.camera = request.form['camera']
        if request.form.has_key('image'):
            editedPhoto.image = request.form['image']
        session.add(editedPhoto)
        session.commit()
        flash('Photo Successfully Edited')
        return redirect(url_for('showPhotos', category_id=category_id))
    else:
        return render_template('editPhoto.html', category_id=category_id, photo_id=photo_id, photo=editedPhoto)

# Delete a photo
@app.route('/category/<int:category_id>/photo/<int:photo_id>/delete', methods=['GET', 'POST'])
def deletePhoto(category_id, photo_id):
    if 'username' not in login_session:
      return redirect('login')
 
    category = session.query(Category).filter_by(id=category_id).one()
    photoToDelete = session.query(Photo).filter_by(id=photo_id).one()
    if request.method == 'POST':
        session.delete(photoToDelete)
        session.commit()
        flash('Photo Successfully Deleted')
        return redirect(url_for('showPhotos', category_id=category_id))
    else:
        return render_template('deletePhoto.html', photo=photoToDelete, category=category)

# JSON API to view all categories
@app.route('/category/JSON')
def categories():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])

# JSON API to view photos for a category
@app.route('/category/<int:category_id>/photos/JSON')
def photosJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    photos = session.query(Photo).filter_by(category_id=category_id).all()
    return jsonify(Photos=[i.serialize for i in photos])

# JSON API to view Photo information
@app.route('/category/<int:category_id>/photo/<int:photo_id>/JSON')
def photoSON(category_id, photo_id):
    photo = session.query(Photo).filter_by(id=photo_id).one()
    return jsonify(Photo=photo.serialize)


# Return a user friendly pretty-printed XML 
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Return a user friendly pretty-printed XML list with parent node named outerName, and with the list of elements
def xmlify(outerName, elemList):
    """Return a pretty-printed XML string for the Element.
    """
    top = Element(outerName)
    for i in elemList:
        top.append(i)

    return prettify(top)

# XM: API to view all categories
@app.route('/category/XML')
def categoriesXML():
    categories = session.query(Category).all()
    return xmlify("categories", [r.serializeXML for r in categories])

# XML API to view photos for a category
@app.route('/category/<int:category_id>/photos/XML')
def photosXML(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    photos = session.query(Photo).filter_by(category_id=category_id).all()
    return xmlify("photos", [r.serializeXML for r in photos])

#XML API to view Photo information
@app.route('/category/<int:category_id>/photo/<int:photo_id>/XML')
def photoXML(category_id, photo_id):
    photo = session.query(Photo).filter_by(id=photo_id).one()
    return prettify(photo.serializeXML)

# Create a new user
def createUser(login_session):
  newUser = User(name = login_session['username'], email=login_session['email'], picture=login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email=login_session['email']).one()
  return user.id

# Get a user from user_id
def getUserInfo(user_id):
  user = session.query(User).filter_by(id=user_id).one()
  return user

# get a user from email address
def getUserID(email):
  try:
    user = session.query(User).filter_by(email=email).one()
    return user.id
  except:
    return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)