from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API', 'temp' : 'something'},
    'todo2': {'task': '?????', 'temp' : 'something'},
    'todo3': {'task': 'profit!', 'temp' : 'something'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('temp')


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 201

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task'], 'temp': args['temp']}
        TODOS[todo_id] = task
        return task, 201

class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo' + str(todo_id)
        if args['task'] != '' and args['temp'] != '':
            TODOS[todo_id] = {
                'task': args['task'],
                'temp': args['temp'],
            }
            return TODOS[todo_id], 201
        else:
            return {'error_message' : 'Invalid Data Format'} , 422

api.add_resource(Todo, '/todos/<todo_id>', endpoint = '/todos/<todo_id>')
api.add_resource(TodoList, '/todos', endpoint = '/todos')


if __name__ == "__main__":
    app.run(debug=True, port=3333)

