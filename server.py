import sys
import argparse
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from pymongo import MongoClient
import urllib

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["geo_database"]
collection = db["places"]

# Custom Request Handler
class MyHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/places':
            # Fetch places from MongoDB
            places = collection.find({})
            output = []
            for place in places:
                output.append({
                    'name': place['name'],
                    'location': place['location']
                })

            # Send JSON response
            self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Geo Spatial Mapping with Python and MongoDB!</h1></body></html>")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json', "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')  # Handle CORS
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())
        
        # Serve the static files
        else:
            super().do_GET()

# Running the server
def run(server_class=HTTPServer, handler_class=MyHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simple HTTP server.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    run(port=args.port)
