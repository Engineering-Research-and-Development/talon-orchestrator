from flask import Flask, redirect

app = Flask(__name__)

from routes.task import task_blueprint
#from routes.monitor import *

app.register_blueprint(task_blueprint)
base_route = '/api/v1'

@app.route('/')
def index():
    #return render_template('index.html')
    return redirect(base_route + '/task-selection')

if __name__ == '__main__':
    app.secret_key = 'keysecret'
    app.run(threaded=True, host='0.0.0.0', port=5004, debug=True)

