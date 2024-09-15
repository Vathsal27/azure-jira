from azurejira import app

@app.route('/')
def hello():
    return {"message":"Hello, World!"}