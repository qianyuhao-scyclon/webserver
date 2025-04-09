import os
from flask import Flask, request, redirect, url_for, flash

from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # Change this to a strong random key for production

def allowed_file(filename):
    """Check if the file has a valid PDF extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Display an HTML form for file uploads."""
    return '''
    <!doctype html>
    <html>
      <head>
        <title>Upload a PDF</title>
      </head>
      <body>
        <h1>Upload a PDF File</h1>
        <form method="post" enctype="multipart/form-data" action="/upload">
          <input type="file" name="file" accept=".pdf">
          <input type="submit" value="Upload">
        </form>
      </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle the uploaded file and present a link to upload another file."""
    if 'file' not in request.files:
        flash('No file part in the request.')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading.')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Use secure_filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return f'''
        <!doctype html>
        <html>
          <head>
            <title>Upload Successful</title>
          </head>
          <body>
            <h1>File "{filename}" uploaded successfully!</h1>
            <p><a href="/">Upload another file</a></p>
          </body>
        </html>
        '''
    else:
        return '''
        <!doctype html>
        <html>
          <head>
            <title>Invalid File</title>
          </head>
          <body>
            <h1>Invalid file type. Only PDF files are allowed.</h1>
            <p><a href="/">Try again</a></p>
          </body>
        </html>
        '''

if __name__ == '__main__':
    # For online access, listen on all available IP addresses.
    app.run(host='0.0.0.0', port=5000, debug=True)
