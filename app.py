from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """

<!DOCTYPE html>

<html>

<head>

    <title>Emotion Music AI</title>

    <style>

        body{
            background:#0f0f0f;
            color:white;
            text-align:center;
            font-family:Arial;
            margin-top:80px;
        }

        h1{
            color:cyan;
            font-size:50px;
        }

        p{
            font-size:25px;
        }

        .box{

            width:70%;
            margin:auto;
            background:#1e1e1e;
            padding:40px;
            border-radius:20px;
            box-shadow:0px 0px 20px cyan;

        }

    </style>

</head>

<body>

    <div class="box">

        <h1>Emotion Music AI</h1>

        <p>Website deployed successfully 🚀</p>

        <p>AI features will be added next.</p>

    </div>

</body>

</html>

"""

@app.route('/')
def home():

    return render_template_string(HTML)

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )