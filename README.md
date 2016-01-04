<H1>Project2</H1>

Project3 is a web application which provides a PostgreSQL database of photo categories and their photos.
Each category has a list of photos which is divided into 3 groups, landscape, portrait and square depending on the dimensions.
A small image is used to display the photo.

The application provides the ability to add, delete, edit and view categories and photos (along with a link to its image)

Only authenticated users may actually edit, delete and add items. Users can authenticate using a Google or Facebook login.

The application provides end points for JSON and XML representations of the data.

The application is also built to prevent CSRF attacks.

<H2>Quick start</H2>
<ul>
<li>
<a href="https://github.com/Afowler2k/udacity-fullstack-p3-catalog/archive/master.zip">Download the latest release</a>
</li>
<li>
Clone the repo: 
<code>
git clone https://github.com/Afowler2k/udacity-fullstack-p3-catalog/archive/master.zip
</code>
</li>
</ul>

<h3>What's included</h3>

Within the download you'll find the following directories and files.
<pre>
<code>
application.py
client_secrets.json
database_setup.py
fb_clients_secrets.json
lotsofphotos.py
README.md
static/styles.css
static/top-banner.jpg
templates/categories.html
templates/deleteCategory.html
templates/deletePhoto.html
templates/editCategory.html
templates/editPhoto.html
templates/header.html
templates/login.html
templates/main.html
templates/newCategory.html
templates/newPhoto.html
templates/photos.html
templates/publiccategories.html
templates/publicPhotos.html
</code>
</pre>

<h3>Running the project</h3>

These files will need to be run inside the Vagrant VM provided by Udacity for this project.<br/>

Install Vagrant and Virtualbox. Instructions can be found on the websites as well as the course materials at https://www.udacity.com/wiki/ud088/vagrant
Clone the fullstack-nanodegree-vm repository. https://github.com/udacity/fullstack-nanodegree-vm 
There is a catalog folder provided for you, but no files have been included. If a catalog folder does not exist, simply create your own inside of the vagrant folder.
Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the terminal). You can find further instructions on how to do so here. ttps://www.udacity.com/wiki/ud088/vagrant

Copy the files from the repo into the catalog folder
Setup the database by typing 'python database_setup.py'
Populate the database by typing 'python lotsofphotos.py'
Run the app by typing 'python application.py'

Access the applcation by going to http://localhost:8000 locally on your browser.

