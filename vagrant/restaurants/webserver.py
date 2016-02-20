import cgi
import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem


class RestaurantsDAO():

    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()



    def close(self):
        #print "closing connection"
        self.session.close()


    def get_all_restaurants(self):
        return self.session.query(Restaurant).all()   


    def get_restaurant(self, rest_id):
        return self.session.query(Restaurant).filter_by(id=rest_id).one()


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



class WebServerHandler(BaseHTTPRequestHandler):

    _HTML_START = "<!DOCTYPE html><html><head></head><body>"
    _HTML_END = "</body></html>"


    def set_dao(dao):
        self.dao = dao


    def _set_get_response_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def _set_post_response_header(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()


    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self._set_get_response_header()

            output = self._HTML_START
            output = "<p><a href='/restaurants/new'>Make a new restaurant</a></p>"

            dao = RestaurantsDAO()
            restaurants = dao.get_all_restaurants()
            dao.close()
            for restaurant in restaurants:
                output += "<p>" 
                output += restaurant.name
                output += "<br/><a href='/restaurants/%s/edit'>Edit</a>" %restaurant.id
                output += "<br/><a href='/restaurants/%s/edit/delete'>Delete</a>" %restaurant.id
                output += "</p>"
            

            output += self._HTML_END

            self.wfile.write(output)
            #print output
            return

        if self.path.endswith("/restaurants/new"):
            self._set_get_response_header()

            output = self._HTML_START
            output += "<h1>Make a new restaurant</h1>"
            output += """<form method='POST' enctype='multipart/form-data'
                        action='/restaurants/new'>
                        <input name='name' type='text'>
                        <input value='Create' type='submit'>
                       </form>"""
            output += self._HTML_END

            self.wfile.write(output)
            return

        if self.path.endswith("/edit"):
            rest_id = self.path.split("/")[2]

            dao = RestaurantsDAO()
            restaurant = dao.get_restaurant(rest_id)
            dao.close()

            if restaurant:
                self._set_get_response_header()
                
                output = self._HTML_START
                output = "<h1>%s</h1>" %restaurant.name
                output += """<form method='POST' enctype='multipart/form-data'
                        action='/restaurants/%s/edit'>
                        <input name='name' type='text' placeholder='%s'>
                        <input value='Rename' type='submit'>
                       </form>""" %(rest_id, restaurant.name)
                output += self._HTML_END

                self.wfile.write(output)
                return

        if self.path.endswith("/delete"):
            rest_id = self.path.split("/")[2]

            dao = RestaurantsDAO()
            restaurant = dao.get_restaurant(rest_id)
            dao.close()

            if restaurant:
                self._set_get_response_header()
                
                output = self._HTML_START
                output = "<h1>Are you sure you want to delete %s</h1>" %restaurant.name
                output += """<form method='POST' enctype='multipart/form-data'
                        action='/restaurants/%s/edit/delete'>
                        <input value='Yes, DELETE' type='submit'>
                       </form>""" %rest_id
                output += self._HTML_END

                self.wfile.write(output)
                return

        if self.path.endswith("/restaurants/id/edit/delete"):
            # TODO: form_delete_restaurant() just confirmation button
            return


      
        self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                # Get new restaurant name
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('name')[0]

                # Insert into DB
                dao = RestaurantsDAO()
                dao.add_restaurant(new_name)
                dao.close()

                self._set_post_response_header()

            if self.path.endswith("/edit"):
                # Get id+new name
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('name')[0]
                    rest_id = self.path.split("/")[2]

                # Update DB
                dao = RestaurantsDAO()
                dao.set_restaurant_name(rest_id, new_name)
                dao.close()

                self._set_post_response_header()

            if self.path.endswith("/delete"):
                # Get id
                rest_id = self.path.split("/")[2]

                # Update DB
                dao = RestaurantsDAO()
                dao.delete_restaurant(rest_id)
                dao.close()

                self._set_post_response_header()

        except AttributeError as e:
            print e
        except NameError as e:
            print e
        except:
            print sys.exc_info()[0]
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()