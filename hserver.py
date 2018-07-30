from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
from mysql.connector import errorcode
 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  config = {
          'user': 'root',
          'password': 'latesnow927',
          'host': '127.0.0.1',
          'database': 'osdb',
          }
  # GET
  def do_GET(self):
        # Send response status code
        imagename = self.path.strip('/')
        if imagename == "nautilus":
            self.send_response(200)
        # Send headers
        #self.send_header('Content-type','text/html')
            self.send_header('Content-type','application/octetstream')
            self.end_headers()
            image = self.run_get(self.config,imagename)
        # Send message back to client
        # Write content as utf-8 data
            #with open('./tmp.iso','rb') as image:
        #self.wfile.write(bytes(message, "utf8"))
                #self.wfile.write(image.read())
            self.wfile.write(image)
        else:
            self.send_response(404)
        return

  def savefile(self,path,data):
    with open(path,"wb") as file:
        file.write(data)

  def run_get(self,config,imagename):
    try:
        con = mysql.connector.connect(**config)
            #imagename = "nautilus"
        query = "SELECT image FROM osimage WHERE Name = %s"
        cursor = con.cursor()
        cursor.execute(query, (imagename,))
        image = cursor.fetchone()[0]
        #self.savefile("tmp.iso",image)
    except mysql.connector.Error as err:
        print(err)
    finally:
        cursor.close()
        con.close()
        return image
 
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 80)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()
