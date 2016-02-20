from flask import Flask
from daos import *

app = Flask(__name__)

rst_dao = RestaurantDAO()
mnu_dao = MenuItemDAO()

@app.route('/')
def HelloWorld():
	return "Hello World!"


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
	items = mnu_dao.get_menu_by_restaurant(restaurant_id)

	output = ""
	for i in items:
		output += "<p>"
		output += "%s</br>" %i.name
		output += "%s</br>" %i.price
		output += "%s" %i.description
		output += "</p>"

	return output


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)