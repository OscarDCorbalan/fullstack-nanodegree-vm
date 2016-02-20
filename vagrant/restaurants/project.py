from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
	if request.method == 'POST':
		new_name = request.form['name']
		mnu_dao.add_menu_item(restaurant_id, new_name)
		return redirect(
			url_for('restaurant_menu', restaurant_id = restaurant_id))

	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
	if request.method == 'GET':
		menu = mnu_dao.get_menu(menu_id)
		return render_template('editmenuitem.html',
								restaurant_id = restaurant_id,
								menu_id = menu_id,
								menu_name = menu.name)

	# Else it's a POST
	new_name = request.form['name']
	mnu_dao.set_menu_name(menu_id, new_name)
	return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
	return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)