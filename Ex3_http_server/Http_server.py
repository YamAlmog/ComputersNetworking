from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
HOST= '0.0.0.0'
PORT= 8080

class MyHttpServer(BaseHTTPRequestHandler):
    sentence = 'Default sentence: Hello from server'
    font_size = '50px'
    color = 'black'

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"<html><body><h1 style=\"font-size: {MyHttpServer.font_size}; color: {MyHttpServer.color}\">{MyHttpServer.sentence}</h1></body></html>", "utf-8"))
        print(MyHttpServer.sentence)
        date= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes(f'Time: {date}', "utf-8"))
    

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
    
        post_data = self.rfile.read(content_length)
        try:
            input_dict = json.loads(post_data.decode('utf-8'))
            print(type(input_dict))
            print(input_dict)

            MyHttpServer.sentence = input_dict['sentence']
            if 'font_size' not in input_dict and 'color' not in input_dict:
                raise KeyError("'font_size' / 'color' should be in POST request parmeters")

            MyHttpServer.font_size = input_dict.get('font_size', MyHttpServer.font_size)
            MyHttpServer.color = input_dict.get('color', MyHttpServer.color)

            # Process user_input here
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'success' : 'True', 'current_sentence': MyHttpServer.sentence}).encode())

        except json.JSONDecodeError as ex:
            response = {'success' : 'False', 'current_sentence': MyHttpServer.sentence, 'error': f" Wrong parameters: {ex}"}
            self.wfile.write(json.dumps(response).encode())  

        except Exception as ex:
            print(f"Error: {ex}")
            self.send_response(400)
            self.end_headers()

            response = {'success' : 'False', 'current_sentence': MyHttpServer.sentence, 'error': str(ex)}
            self.wfile.write(json.dumps(response).encode())  
        
server= HTTPServer((HOST,PORT), MyHttpServer)

print("Server now running...")
server.serve_forever()
server.server_close()
