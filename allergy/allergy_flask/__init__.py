import os, sys
import openai

from flask import Flask
from flask import (
     redirect, render_template, request, session,
)

API_KEY = open("./allergy_flask/API_KEY.txt", "r").read()
openai.api_key = API_KEY

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/', methods=('GET','POST'))
    def recipe():
        DEFAULT_ALLERGENS =['Nut','Dairy','Egg','Wheat','Soy','Gluten']
        if request.method == 'POST':
            user_recipe = request.form['user_recipe']
            allergies = request.form.getlist('allergylist')

            other_allergies = request.form['other_allergies']
            other_allergies = other_allergies.split(" ")
            print(allergies.extend(other_allergies))
            query = "make a recipe for {} that does not contain {}.".format(
                         user_recipe,', '.join(allergies))
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides recipes."}, 
                    {"role": "user", "content": query}
                ],

            )
            #print(str(response).split('contents='))
            recipe = response.choices[0].message.content
            user_var = 'Fred'
            
        else:
            user_var = None
            user_recipe=""
            allergies = []
            other_allergies = ""
            recipe=''
        
        return render_template('home.html', response = recipe, user_recipe = user_recipe,
                               allergies = allergies, default_allergens=DEFAULT_ALLERGENS)


    return app


