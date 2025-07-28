import json
import os

from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate

from models import db, JsonData

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json_data = request.form['json_data']

        try:
            data = json.loads(json_data)
            item = data[0]
            try:
                if len(item['name']) >= 50:
                    return "Error: name is more then 50 symbols", 400

                date = datetime.strptime(item['date'], '%Y-%m-%d_%H:%M')
                db.session.add(JsonData(name=item['name'], date=date))

            except (KeyError, ValueError) as e:
                return f"Data error: {str(e)}", 400

            db.session.commit()
            return redirect(url_for('show_data'))

        except json.JSONDecodeError:
            return "Invalid JSON", 400

    return render_template('index.html')


@app.route('/data')
def show_data():
    data = JsonData.query.all()
    return render_template('data.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)