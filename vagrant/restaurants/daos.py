from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


class GenericDAO():

    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()


    def close(self):
        #print "closing connection"
        self.session.close()

class RestaurantDAO(GenericDAO):

    def get_restaurant(self, rest_id):
        return self.session.query(Restaurant).filter_by(id=rest_id).one()


    def get_first_restaurant(self):
        return self.session.query(Restaurant).first()


    def get_all_restaurants(self):
        return self.session.query(Restaurant).all()


    def set_restaurant_name(self, rest_id, new_name):
        restaurant = self.get_restaurant(rest_id)
        if restaurant:
            restaurant.name = new_name
            self.session.add(restaurant)
            self.session.commit()


    def add_restaurant(self, new_name):
        new_restaurant = Restaurant(name = new_name)
        self.session.add(new_restaurant)
        self.session.commit()


    def delete_restaurant(self, rest_id):
        restaurant = self.get_restaurant(rest_id)
        if restaurant:
            self.session.delete(restaurant)
            self.session.commit()



class MenuItemDAO(GenericDAO):

    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    
    def close(self):
        #print "closing connection"
        self.session.close()


    def get_menu(self, menu_id):
        return self.session.query(MenuItem).filter_by(id=menu_id).one()


    def get_menu_by_restaurant(self, rest_id):
        return self.session.query(MenuItem).filter_by(restaurant_id = rest_id)


    def set_menu_name(self, menu_id, new_name):
        menu = self.get_menu(menu_id)
        if menu:
            menu.name = new_name
            self.session.add(menu)
            self.session.commit()


    def add_menu_item(self, rest_id, new_name):
        new_menu = MenuItem(name = new_name, restaurant_id = rest_id)
        self.session.add(new_menu)
        self.session.commit()