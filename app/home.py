def home_page(name):
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
            }

            .container {
                max-width: 400px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            h1 {
                text-align: center;
            }

            .form-group {
                margin-bottom: 20px;
            }

            .form-group p {
                margin-bottom: 5px;
            }

            .form-group input[type="text"] {
                width: 95%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }


            .form-group input[type="submit"] {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: #fff;
                border: none;
                border-radius: 3px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome ''' + name + '''!</h1>
            <form action="http://localhost:5000/results" method="get">
                <div class="form-group">
                    <p>Enter team name:</p>
                    <p><input type="text" name="nm" /></p>
                </div>
                <div class="form-group">
                    <p>Enter year:</p>
                    <p><input type="text" name="year" /></p>
                </div>
                <div class="form-group">
                    <p><input type="submit" value="submit" /></p>
                </div>
            </form>
        </div>
    </body>
    </html>'''