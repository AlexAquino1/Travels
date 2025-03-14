import sys 
sys.dont_write_bytecode = True
from FlaskCode import app


if __name__ == "__main__":
    app.run(debug=True)
