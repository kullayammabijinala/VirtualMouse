from flask import Flask, render_template
import threading
import virtual_mouse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/start')
def start_mouse():
    threading.Thread(target=virtual_mouse.start_mouse).start()
    return "Virtual Mouse Started!"

if __name__ == '__main__':
    app.run(debug=True)
