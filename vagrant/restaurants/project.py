from flask import Flask, render_template
from daos import RestaurantDAO, MenuItemDAO

app = Flask(__name__)

rst_dao = RestaurantDAO()
mnu_dao = MenuItemDAO()

@app.route('/')
def HelloWorld():
	return "Hello World!"


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
	restaurant = rst_dao.get_restaurant(restaurant_id)
	items = mnu_dao.get_menu_by_restaurant(restaurant_id)

	return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurants/<int:restaurant_id>/new/')
def new_menu_item(restaurant_id):
	return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
	return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
	return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)