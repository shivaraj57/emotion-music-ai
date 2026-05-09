from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Emotion Music AI</title>
        <style>
            body{
                background:black;
                color:white;
                text-align:center;
                font-family:Arial;
                margin-top:100px;
            }

            h1{
                color:cyan;
                font-size:50px;
            }

            p{
                font-size:25px;
            }
        </style>
    </head>

    <body>

        <h1>Emotion Music AI</h1>

        <p>Website is Live Successfully 🚀</p>

    </body>
    </html>
    """

if __name__ == '__main__':

    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )