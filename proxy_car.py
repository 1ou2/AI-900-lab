from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
from urllib.parse import parse_qs
from dotenv import load_dotenv

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    load_dotenv()
    endpoint = os.getenv('ENDPOINT')
    api_key = os.getenv('API_KEY')
    AZURE_ENDPOINT = endpoint
    API_KEY =  api_key # Replace with your actual API key
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Forward the request to Azure
            azure_response = requests.post(
                self.AZURE_ENDPOINT,
                data=post_data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.API_KEY}'
                }
            )

            # Send the response back to the client
            self.send_response(azure_response.status_code)
            self.send_cors_headers()
            
            # Only forward non-CORS headers from the Azure response
            for header, value in azure_response.headers.items():
                if not header.lower().startswith('access-control-'):
                    self.send_header(header, value)
            
            self.end_headers()
            self.wfile.write(azure_response.content)

        except Exception as e:
            self.send_error(500, str(e))

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print(f'Starting proxy server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
