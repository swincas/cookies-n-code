GUI_cookiesncode.py

On OzStar:
bokeh serve --allow-websocket-origin=localhost:3112 --port=3112 GUI_cookiesncode.py --args -csv computers.csv

Forward localhost:3112 to local computer
On local machine:
ssh -L 3112:localhost:3112 ozstar



