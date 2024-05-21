from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'},
    {'id': 2, 'name': 'Flash', 'category': 'cat'}
]


class PetIn(Schema):
    name = String(required=True, validate=Length(0, 10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()

@app.get('/')
def say_hello():
    return {'message': 'Helloaaaa!'}


@app.get('/pets/<int:pet_id>')
@app.output(PetOut)
def get_pet(pet_id):
    if pet_id > len(pets) - 1 or pets[pet_id].get('deleted'):
        abort(404)
    return pets[pet_id]


@app.get('/pets')
@app.output(PetOut(many=True))
def get_pets():
    return pets

@app.post('/pets')
@app.input(PetIn, location='json')
@app.output(PetOut, status_code=201)
def create_pet(json_data):
    pet_id = len(pets)
    json_data['id'] = pet_id
    pets.append(json_data)
    return pets[pet_id]


@app.patch('/pets/<int:pet_id>')
@app.input(PetIn(partial=True), location='json')
@app.output(PetOut)
def update_pet(pet_id, json_data):
    if pet_id > len(pets) - 1:
        abort(404)
    for attr, value in json_data.items():
        pets[pet_id][attr] = value
    return pets[pet_id]

@app.delete('/pets/<int:pet_id>')
@app.output({}, status_code=204)
def delete_pet(pet_id):
    if pet_id > len(pets) - 1:
        abort(404)
    pets[pet_id]['deleted'] = True
    pets[pet_id]['name'] = 'Ghost'
    return ''

@app.route('/sql')
def sql():
    server = open('/bindings/mysql/host').read()
    user = open('/bindings/mysql/username').read()
    passwd = open('/bindings/mysql/password').read()
    dbname =  open('/bindings/mysql/database').read()
    print(f'using {server} / {user} / {passwd} / {dbname}')
    try:
        db = MySQLdb.connect(server, user, passwd, dbname)
        cursor = db.cursor()        
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
    # Check if anything at all is 
        return 'OK'              
    except:
        return "ERROR IN CONNECTION"


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
