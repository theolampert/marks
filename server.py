import json
import os
from app import create_bookmark, get_bookmarks
from http.server import BaseHTTPRequestHandler, HTTPServer


port = os.getenv('PORT', default=8080)
class RequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
        self.send_response(200)

        path = self.path

        if path == '/bookmarks':
            self.send_header('Content-type', 'application/json')
            message = json.dumps(get_bookmarks())
        elif path == '/tags':
            self.send_header('Content-type', 'application/json')
            message = json.dumps(get_tags())
        elif path == '/urls':
            self.send_header('Content-type', 'application/json')
            message = json.dumps(get_urls())

        self.end_headers()
        self.wfile.write(bytes(message, 'utf8'))
        return

  def do_POST(self):
        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        path = self.path
        data = json.loads(self.data_string)

        if path == '/bookmarks':
            create_bookmark(data['url'], data['tags'])
            message = json.dumps(data)
        else:
            message = json.dumps('Unsupported.')

        self.wfile.write(bytes(message, 'utf8'))
        return

  def do_DELETE(self):
      self.send_response(200)
      return

def run():
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('🌺 Starting server on port {}'.format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
