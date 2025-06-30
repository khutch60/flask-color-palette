from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms.fields import SubmitField, URLField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import URL, InputRequired
import os
import requests
from palette import get_palette

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, '/uploads')

photo = UploadSet('photos', IMAGES)
configure_uploads(app, photo)
patch_request_class(app)

class UrlForm(FlaskForm):
    image_url = URLField("Enter Image URL", validators=[InputRequired(), URL()], render_kw={"placeholder": "Photo URL"} )
    submit = SubmitField()

class UploadForm(FlaskForm):
    image_file = FileField(validators=[FileRequired(), FileAllowed(photo, 'Images only!')])
    submit = SubmitField('Submit')


@app.route('/', methods=["GET"])
def index():
    url_form = UrlForm()
    upload_form = UploadForm()

    return render_template('index.html', url=url_form, upload=upload_form)

@app.route("/url", methods=["POST"])
def url():
    url_form = UrlForm()
    if url_form.validate_on_submit():
        image_url = url_form.image_url.data
        return redirect(url_for("image", image=image_url))

@app.route("/upload", methods=["POST"])
def upload_image():
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        filename = photo.save(upload_form.image_file.data)
        image_url = photo.url(filename)
        return redirect(url_for("image", image=image_url))

@app.route('/image')
def image():
    image_url = request.args.get('image', None)
    response = requests.get(image_url)
    palette = get_palette(img=response)
    return render_template("image.html", image=image_url, palette=palette)


if __name__ == "__main__":
    app.run(debug=True)



