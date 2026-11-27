from flask import Flask
from flask_cors import CORS
from disciplinas import disciplinas_bp
from matricula import matricula_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(matricula_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
