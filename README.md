# Team *Dragonfly* Small Group project

## Team members
The members of the team are:
- *Zakariya Ahmed Mohamed*
- *Ammar Alshareef*
- *Seif Eunice*
- *Said Mammadov*
- *Rohit Pun*
- *Taseen Rahman*

## Project structure
The project is called `system`.  It currently consists of a single app `clubs`.

## Deployed version of the application
The deployed version of the application can be found at https://pacific-lake-90367.herokuapp.com

The deployed version of the admin page can be found at https://pacific-lake-90367.herokuapp.com/admin/


## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

Inspiration taken from clucker videos on Keats.

