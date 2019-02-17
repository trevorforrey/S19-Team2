from flask import Flask, render_template, request, Response, send_from_directory, redirect, url_for
from spyce import spyce
import os, fnmatch

CURRENT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
template_path = os.path.abspath(CURRENT_PATH + "/dist")
app = Flask(__name__, template_folder=template_path, static_url_path='', static_folder=None)
spy = spyce.spyce()
SPK_FILENAME = "spacecraft.spk"
TRAJECTORY_FOLDER = CURRENT_PATH + "/data/trajectory/"
spy_loaded = False

#loading initial file for spy
#snippet derived from https://stackoverflow.com/questions/1724693/find-a-file-in-python
def load_spacecraft_spk():
    for root, dirs, files in os.walk(TRAJECTORY_FOLDER):
        if "spacecraft.spk" in files:
                spy.main_file = os.path.join(root, SPK_FILENAME)
                spy_loaded = True

@app.route('/')
def root():
    return "This is the root endpoint for this server. You probably shouldn't be here. try /dist/index.html"

@app.route('/dist/index.html', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/spacecraft/pos', methods=['GET'])
def get_spacecraft_pos():
    return "TODO"

#code derived from http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
@app.route('/data/trajectory', methods=['GET', 'POST'])
def change_trajectory_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print ("[WARN]: No file recieved.")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print ("[WARN]: No file selected.")
            return redirect(request.url)
        if file and file.filename[-4:] == ".spk":
            file.save(os.path.join(TRAJECTORY_FOLDER, SPK_FILENAME))
            #TODO: replace with actual webpages
            try:
                load_spacecraft_spk()
                return "File change successful!"
            except:
                return "Unable to use SPK file"
        print ("[WARN]: improper file format")

    #TODO: replace with actual webpage.
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@app.route('/<path:filename>', methods=['GET'])
def get_file(filename):
    print("PATH: " + filename)
    print (filename[-3:])
    if (filename[-3:] == ".js" or
            filename[-4:] == ".jpg" or
            filename[-4:] == ".map" or
            filename[-4:] == ".ico"):

        return send_from_directory('dist', filename)
    return "OOOPSIE WOOOPSIE!"


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
    try:
        load_spacecraft_spk()
    except:
        print ("[WARN]: Unable to load SPK file")