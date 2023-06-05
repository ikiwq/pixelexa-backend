# Pixelexa
## Introduction
Pixelexa is an open-source online newspaper inspired by the Washington Post. It was meant to give the users an opportunity to publish articles of all kinds without the need to be an actual reporter. 
The user can interact with the articles: read them, star them, comment on them, and filter them by a specific text or by a category.

#### Source code
This is the frontend repository, and the backend repository can be found [here](https://github.com/ikiwq/pixelexa-frontend).

## Installation
### Getting the files and the requisites
Clone the repository:

    git clone https://github.com/[username]/[project-name].git
Go to the project directory and install the necessary dependencies using pip:

    pip install flask
    pip install marshmallow

### Configuration
Before starting the app, we have to do a little bit of configuration.

Inside the app.py file in the project directory, there are some fields we need to modify:

#### Secret key
    app.config['SECRET_KEY'] = 'your_secret_ket'

The secret key will be used to generate and decode JWTs.

#### Database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_connector://your_username:your_password@your_db_url/your_db'
This field is used to provide your flask with a database. A valid example would be:

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:80/pixelexa'
#### Static file folder
    app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static', 'uploads')
This field defines the folder where all the images will be stored and retrieved.
#### Change the port
    if __name__ == '__main__':
      app.run(port=5000)
To change the port, at the end of the main.py file modify the app.run() params.

### Usage
Start the application:

    mvn spring-boot:run
      
Access the application in your web browser at http://localhost:5000 or the port you specified in the main.py file, and you're ready to go!

