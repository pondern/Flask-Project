from flask import Flask, request, jsonify
from peewee import * 
from playhouse.shortcuts import model_to_dict, dict_to_model
from datetime import date
db = PostgresqlDatabase('people', user='Johnny_Appleseed',
                        password='123456', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    birthday = DateField()
    age = IntegerField()


db.connect()
db.drop_tables([Person])
db.create_tables([Person])

Person(name='Raul', birthday=date(1990, 1, 1), age=1000).save()
Person(name='Chris', birthday=date(1985, 5, 10), age=1000).save()
Person(name='Mega Hawk', birthday=date(1980, 12, 25), age=9999).save()


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/person/', methods=['GET', 'POST'])
@app.route('/person/', methods=['GET', 'PUT', "DELETE"])
def endpoint(id=None):  
    if request.method == 'GET':
        if id: 
            return jsonify(model_to_dict(Person.get(Person.id == id)))
        else:  
            people_list = []
            for people in Person.select():
                people_list.append(model_to_dict(people))
            return jsonify(people_list)
    if request.method == 'PUT':
        body = request.get_json()
        Person.update(body).where(Person.id == id).execute()
        return "Person" + str(id) + "has been updated"
    if request.method == 'POST':
        new_person = dict_to_model(Person, request.get_json())
        new_person.save()
        return jsonify({"Success: True"})
    if request.method == 'DELETE':
        Person.delete().where(Person.id == id).execute()
        return "Person " + str(id) + " deleted."


app.run(debug=True)

