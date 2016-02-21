from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from daos import RestaurantDAO, MenuItemDAO

app = Flask(__name__)
rst_dao = RestaurantDAO()
mnu_dao = MenuItemDAO()


# API Endpoints serving JSON

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
	items = mnu_dao.get_menu_by_restaurant(restaurant_id)
	return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
	item = mnu_dao.get_menu(menu_id)
	return jsonify(MenuItem=item.serialize)



# Web routes

# Our index, shows a list of all the restaurants, plus restaurant create/edit/delete links
@app.route('/')
@app.route('/restaurants')
def show_restaurants():
	restaurants = rst_dao.get_all_restaurants()
	return render_template('restaurants.html', restaurants = restaurants)


# Form to create a new restaurant
@app.route('/restaurants/new')
def new_restaurant():
	return "TODO: form to add a restaurant"


# Form to edit an existing restaurant
@app.route('/restaurants/<int:restaurant_id>/edit')
def edit_restaurant(restaurant_id):
	return "TODO: editing restaurant %s" %restaurant_id


# Form to delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete')
def delete_restaurant(restaurant_id):
	return "TODO: delete restaurant %s" %restaurant_id


# List of the menu items in a restaurant, plus item create/edit/delete links
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def show_menu(restaurant_id):
	restaurant = rst_dao.get_restaurant(restaurant_id)
	items = mnu_dao.get_menu_by_restaurant(restaurant_id)

	return render_template('menu.html', restaurant = restaurant, items = items)


# Form to create a new menu item in the restaurant
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
	if request.method == 'GET':
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)
	
	# Else it's a POST
	new_name = request.form['name']
	mnu_dao.add_menu_item(restaurant_id, new_name)
	flash("New menu item created")

	return redirect(
		url_for('restaurant_menu', restaurant_id = restaurant_id))


# Form to edit an existing menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
	if request.method == 'GET':
		return render_template('editmenuitem.html',
								restaurant_id = restaurant_id,
								menu_id = menu_id,
								menu_name = mnu_dao.get_menu(menu_id).name)

	# Else it's a POST
	new_name = request.form['name']
	mnu_dao.set_menu_name(menu_id, new_name)
	flash("Menu item succesfully edited")
	return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))


# Form to delete an existing menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
	if request.method == 'GET':
		menu = mnu_dao.get_menu(menu_id)
		return render_template('deletemenuitem.html', menu = menu)

	# Else it's a POST
	mnu_dao.delete_menu(menu_id)
	flash("Menu item deleted")
	return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))


if __name__ == '__main__':
	app.secret_key = 'super_insecure_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)