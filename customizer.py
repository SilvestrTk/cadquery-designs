from flask import Flask, request, render_template, send_file
import os
from tube_holder import TubeHolder

app = Flask(__name__)
EXPORT_FILE = "generated_model.stl"

@app.route('/', methods=['GET', 'POST'])
def index():
    global EXPORT_FILE
    message = ""
    if request.method == 'POST':
        try:
            width = float(request.form['width'])
            height = float(request.form['height'])
            diameter = float(request.form['diameter'])

            if diameter * 2 + 10 >= width:
                message = "Error: diameter * 2 + 10 must be less than width"
            else:
                # Generate CadQuery object
                model = TubeHolder(bwidth=width, bheight=height, diameter=diameter)
                model.add_holes().finalize()
                #create directory if it doesn't exist
                if not os.path.exists("tube_holders"):
                    os.makedirs("tube_holders")
                # Set export file path
                EXPORT_FILE = f"tube_holders/tube_holder_{str(width).replace('.', '_')}x{str(width).replace('.', '_')}x{str(height).replace('.', '_')}d{str(diameter).replace('.', '_')}.stl"
                # Export the model
                model.export(EXPORT_FILE)
                print(EXPORT_FILE)
                return render_template('index.html', message="STL generated!", download_link="/download")
        except ValueError:
            message = "Please enter valid numbers."
    
    return render_template('index.html', message=message)

@app.route('/download')
def download():
    return send_file(EXPORT_FILE, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
