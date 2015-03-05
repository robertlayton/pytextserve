#!/usr/bin/env python3
import time
import os

from http.server import BaseHTTPRequestHandler, HTTPServer


datadir = os.path.join(os.path.expanduser("~"), "tmp", "results")

class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            idv = int(self.path[1:])
        except:
            idv = 0
        filenames = os.listdir(datadir)
        filename = os.path.join(datadir, filenames[idv])
        
        with open(filename) as inf:
            content = inf.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        code = "<head><script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js\"></script></head><body id=all>{script}Filename: {filename}<br><a id=prev href=\"{prevlink}\">Previous</a>&nbsp&nbsp&nbsp&nbsp<a id=next href=\"{nextlink}\">Next  </a><pre>{content}</pre>"
        
        prevlink = "/{}".format(idv-1)
        nextlink = "/{}".format(idv+1)
        
        script = """
                    <script>
                    $(document).keypress(function(e) {
                        var code = e.keyCode || e.which;
                        if(code == 39) { //Right arrow keycode
                            window.location = $("#next").attr("href");
                        }else if (code == 37){ // Left arrow
                            window.location = $("#prev").attr("href");
                        }
                        
                    });
                    </script>
                """
        code = code.format(script=script, filename=filename, prevlink=prevlink, nextlink=nextlink, content=content)
        
        self.wfile.write(code.encode())

    def do_POST(self):
        return do_GET(self)


port = 8080
selflink = "http://localhost:{}".format(port)
print(selflink)
server = HTTPServer(('', port), StoreHandler)
server.serve_forever()
