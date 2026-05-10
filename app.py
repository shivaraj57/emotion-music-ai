from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    filename = None

    if request.method == 'POST':

        image = request.files['image']

        if image:

            os.makedirs("static/uploads", exist_ok=True)

            filepath = os.path.join("static/uploads", image.filename)

            image.save(filepath)

            filename = image.filename

    return render_template(
        "index.html",
        filename=filename
    )

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )