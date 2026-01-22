#!/usr/bin/env python3
"""
CORS-enabled HTTP server for Performance Dashboard
Allows the dashboard to fetch files from local folder
"""

import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
import sys

PORT = 8080

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    try:
        with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
            print("╔════════════════════════════════════════════════════════════╗")
            print("║       Performance Dashboard - Local Server Running        ║")
            print("╚════════════════════════════════════════════════════════════╝")
            print(f"\n  📂 Serving folder: {sys.path[0]}")
            print(f"  🌐 URL: http://localhost:{PORT}")
            print(f"  📄 Files available: Check files.json")
            print(f"\n  ℹ️  Use this URL in the dashboard's 'Local Folder' option")
            print(f"  ⏹️  Press Ctrl+C to stop the server\n")
            print("─" * 60)
            print("Requests:\n")

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"\n❌ Error: Port {PORT} is already in use!")
            print(f"   Stop the existing server or use a different port.\n")
        else:
            print(f"\n❌ Error starting server: {e}\n")
        sys.exit(1)
