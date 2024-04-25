from aiohttp import web, ClientSession
import datetime

def write_log(log_message):
    with open("honeypot.log", "a") as log_file:
        log_file.write(log_message + "\n")


# Handler pour le honeypot
async def handle_request(request):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remote_address = request.remote
    method = request.method
    path = str(request.rel_url)
    version = f"HTTP/{request.version.major}.{request.version.minor}"
    user_agent = request.headers.get("User-Agent", "Unknown")

    response_text = "You've been trapped!"
    response_status = 200

    log_message = f"[{timestamp}] - [{remote_address}] - [{method} {path} {version} {response_status}] - [{user_agent}]"

    print(log_message)
    write_log(log_message)  # local logging

    return web.Response(text=response_text, status=response_status)


async def create_app():
    app = web.Application()
    app.router.add_get('/', handle_request)  # Traite les requêtes GET sur la racine
    return app

# Lancement du honeypot
if __name__ == "__main__":
    app = create_app()
    web.run_app(app, port=80)
