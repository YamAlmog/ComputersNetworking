from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
HOST= 'localhost'
PORT= 8080

class MyHttpServer(BaseHTTPRequestHandler):
    sentence = 'Default sentence: Hello from server'

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"<html><body><h1 style=\"font-size: 60px;\">{MyHttpServer.sentence}</h1></body></html>", "utf-8"))
        print(MyHttpServer.sentence)
        date= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes(f'Time: {date}', "utf-8"))
    

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        post_data = self.rfile.read(content_length)
        try:
            input_dict = json.loads(post_data.decode('utf-8'))
            print(input_dict)

            MyHttpServer.sentence = input_dict['sentence']
            #font_size = input_dict['font_size']
            #color = input_dict['color']
            # Process user_input here
            self.send_response(200)
            self.end_headers()

            # Send response to client in that JSON format:
            # {'success' : 'True/False', 'current_sentence': 'SENTENCE'}
            self.wfile.write(json.dumps({'success' : 'True', 'current_sentence': MyHttpServer.sentence}).encode())
        except Exception as ex:
            print(f"Error: {ex}")
            self.send_response(400)
            self.end_headers()

            # Send response to client in that JSON format:
            # {'success' : 'True/False', 'current_sentence': 'SENTENCE'}
            self.wfile.write(json.dumps({'success' : 'False', 'current_sentence': MyHttpServer.sentence}).encode())  
        
server= HTTPServer((HOST,PORT), MyHttpServer)

print("Server now running...")
server.serve_forever()
server.server_close()
