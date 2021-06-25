import os

from flask import Flask


def create_app(test_config=None):
	#create and configure the app
	app = Flask(__name__,instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE = os.path.join(app.instance_path,'flaskr.sqlite'),
	)

	if test_config is None:
		#Load the instance config if it exists
		app.config.from_pyfile('config.py', silent=True)
	else:
		#Load the test config if passed
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	from . import db
	db.init_app(app)

	from . import auth, blog
	app.register_blueprint(auth.bp)
	app.register_blueprint(blog.bp)

	app.add_url_rule('/',endpoint='index')

	return app
	