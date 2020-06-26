# drf-blog-post
Simple api for a Django blogging app for testing my new module post

 ![blog](https://github.com/kkosiba/blog-django/blob/master/pics/main.png)

Features
--------
1. Basic User authorisation and registration.
2. Basic User, Group permissions: admin, editor, normal.
	- Editors: is a Group. User of this group can add posts, update/delete the existing 
	  posts for which they have permissions/ownership.
	- admin: is superuser as usual.
	- normal user can add comments and like posts
3. Facebook comments.
4. Tags.
5. Post History.
6. Search, year/month archives.
7. Sort by post author, category, tags.
8. Basic REST API provided by Django REST framework (available at `/api`).
9. Contact us page (configurable).


Planned Modules
----------
Blog pages

google analytics

SEO compliant

Dynamic Menu.

Social Login.


Main requirements
------------

1. `python` 3.5, 3.6, 3.7
2. `Django` 2.2.13
3. `PostreSQL` 11.1

This project also uses a few external packages (see `requirements.txt` file for details).
For instance, tags support is provided by [django-taggit](https://github.com/alex/django-taggit).


## How to set up

### Setup using Docker

The easiest way to get this project up and running is via [Docker](https://www.docker.com/). See [docs](https://docs.docker.com/get-started/) to get started. Once set up run the following command:

`docker-compose up`

It may take a while for the process to complete, as Docker needs to pull required dependencies. Once it is done, the application should be accessible at `0.0.0.0:8000`. 

### Manual setup

Firstly, create a new directory and change to it:

`mkdir blog-django && cd blog-django`

Then, clone this repository to the current directory:

`git clone https://github.com/agiledesign2/django-blog-post.git .`


Next, one needs to setup database like SQLite or PostgreSQL on a local machine. This project uses PostgreSQL by default (see [Django documentation](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) for different setup). This process may vary from one OS to another, eg. on Arch Linux one can follow a straightforward guide [here](https://wiki.archlinux.org/index.php/PostgreSQL).

The database settings are specified in `website/settings/dev.py`. In particular the default database name is `BlogDjango`, which can be created from the PostgreSQL shell by running `createdb BlogDjango`.


Next, set up a virtual environment and activate it:

`python3 -m venv env && source env/bin/activate`

Install required packages:

`pip3 install -r requirements.txt`

Next, perform migration:

`python3 manage.py migrate --settings=website.settings.dev`

The setup is complete. Run a local server with

`python3 manage.py runserver --settings=website.settings.dev`

The blog should be available at `localhost:8000`.

## What's next?

At this point you can create a superuser account, the Editors group, add a user to this group and create a normal user to this group.
You can do all this with `python3 manage.py makesuper`.

1. This command create 
	- A admin user with user name: admin with password: admin.
	- A normal user name: editor with password: editor and added it to the Editor group.
	- A normal user name: normal with password normal.