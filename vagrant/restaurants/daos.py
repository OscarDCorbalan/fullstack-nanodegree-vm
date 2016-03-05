from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User


class GenericDAO():

    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()


    def close(self):
        #print "closing connection"
        self.session.close()


    def persist(self, obj):
        self.session.add(obj)
        self.session.commit()


    def discontinue(self, obj):
        self.session.delete(obj)
        self.session.commit()



class UserDAO(GenericDAO):

    def get_user(self, user_id):
        return self.session.query(User).filter_by(user_id = user_id).one()


    def get_user_id(self, email):
        try:
            return self.session.query(User).filter_by(email = email).one().id
        except:
            return None


    def add_user(self, name, email, picture):
        new_user = User(name = name, email = email, picture = picture)
        self.persist(new_user)
        return self.get_user_id(email)



class RestaurantDAO(GenericDAO):

    def get_restaurant(self, rest_id):
        return self.session.query(Restaurant).filter_by(id = rest_id).one()


    def get_first_restaurant(self):
        return self.session.query(Restaurant).first()


    def get_all_restaurants(self):
        return self.session.query(Restaurant).all()


    def set_restaurant_name(self, rest_id, new_name):
        restaurant = self.get_restaurant(rest_id)
        if restaurant:
            restaurant.name = new_name
            self.persist(restaurant)


    def add_restaurant(self, new_name, user_id):
        new_restaurant = Restaurant(name = new_name, user_id = user_id)
        self.persist(new_restaurant)


    def delete_restaurant(self, rest_id):
        restaurant = self.get_restaurant(rest_id)
        if restaurant:
            self.discontinue(restaurant)



class MenuItemDAO(GenericDAO):

    def get_menu(self, menu_id):
        return self.session.query(MenuItem).filter_by(id=menu_id).one()


    def get_menu_by_restaurant(self, rest_id):
        return self.session.query(MenuItem).filter_by(restaurant_id = rest_id).all()


    def get_menu_name(self, menu_id):
        menu = self.get_menu(menu_id)
        return menu.name


    def get_menu_description(self, menu_id):
        menu = self.get_menu(menu_id)
        return menu.description


    def get_menu_price(self, menu_id):
        menu = self.get_menu(menu_id)
        return menu.price


    def get_menu_course(self, menu_id):
        menu = self.get_menu(menu_id)
        return menu.course


    def get_menu_image(self, menu_id):
        menu = self.get_menu(menu_id)
        return menu.filename


    def set_menu_name(self, menu_id, new_name):
        menu = self.get_menu(menu_id)
        if menu:
            menu.name = new_name
            self.persist(menu)


    def set_menu_description(self, menu_id, new_description):
        menu = self.get_menu(menu_id)
        if menu:
            menu.description = new_description
            self.persist(menu)


    def set_menu_price(self, menu_id, new_price):
        menu = self.get_menu(menu_id)
        if menu:
            menu.price = new_price
            self.persist(menu)


    def set_menu_course(self, menu_id, new_course):
        menu = self.get_menu(menu_id)
        if menu:
            menu.course = new_course
            self.persist(menu)


    def set_menu_image(self, menu_id, filename):
        menu = self.get_menu(menu_id)
        if menu:
            menu.image = filename
            self.persist(menu)


    def add_menu_item(self, rest_id, new_name, user_id):
        new_menu = MenuItem(name = new_name, restaurant_id = rest_id, user_id = user_id)
        self.persist(new_menu)


    def delete_menu(self, menu_id):
        menu = self.get_menu(menu_id)
        if menu:
            self.discontinue(menu)
