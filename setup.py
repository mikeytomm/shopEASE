'''to start the web server'''
from shopeaseapp import app
#instanting an object of flask
if __name__ =="__main__":
    app.run(debug=True, port=5000)  