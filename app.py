import os
from flask import Flask, g, render_template, redirect, request, jsonify
import db
import access

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='co-bot-is-the-best',
    )
    db.init_app(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app


app = create_app()


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        record_confirmed = request.form.get("record_confirmed") != None
        record_fatalities = request.form.get("record_fatalities") != None
        top_5_most_confirmed = request.form.get("top_5_most_confirmed") != None
        top_5_most_fatalities = request.form.get("top_5_most_fatalities") != None
        top_5_least_confirmed = request.form.get("top_5_least_confirmed") != None
        top_5_least_fatalities = request.form.get("top_5_least_fatalities") != None
        total_fatalities_highest = request.form.get("total_fatalities_highest") != None
        total_confirmed_highest = request.form.get("total_confirmed_highest") != None
        error = db.register_user(email, record_confirmed, record_fatalities,
        top_5_most_confirmed, top_5_most_fatalities,
        top_5_least_confirmed, top_5_least_fatalities,
        total_fatalities_highest, total_confirmed_highest, None)
        if error is None:
            return redirect('/landing')
        else:
            if error.args[0] == 1062:
                dup_property = 'email'
                error_msg = ('There is already an account'
                        ' with that {}.'.format(dup_property))
            return render_template(
                'register.html',
                error=error_msg,
            )
    return render_template('register.html')


@app.route('/landing')
def landing():
    return render_template(
        'landing.html'
    )

if __name__ == '__main__':
    app.run()
