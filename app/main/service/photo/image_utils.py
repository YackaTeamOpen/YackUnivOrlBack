# Image tool routines
# Olivier - Février-Juin 2022
import base64
from PIL import Image
from io import BytesIO
import re

from main import db
from main.config import environments, config_name
from main.model.user import User

def upload_user_photo(user_id, file_basename, extension) :
    """ Upload a user's avatar in the database """
    absolute_file_path = (environments[config_name]["api_app_path"] +
        "../install/uploads/" + (file_basename + user_id + "." + extension))

    with open(absolute_file_path, 'rb') as imagefile:
        base64string = base64.b64encode(imagefile.read()).decode('ascii')
        avatar_size = environments[config_name]["avatar_size"]
        lightened_image = lighten_image(base64string, avatar_size)

    print(lightened_image)  # print base64string to console
    # Will look something like:
    # iVBORw0KGgoAAAANS  ...  qQMAAAAASUVORK5CYII=

    # Save it into DB
    data = {"photo": lightened_image}
    User.query.filter_by(id = user_id).update(data)
    db.session.commit()


def lighten_image(image_data, size) :
    """ Returns an size-reduced version of an image """
    bytes_image = Image.open(BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', image_data))))
    max_size = max(bytes_image.size)
    if max_size < size :
        return image_data
    red_factor = int(max_size / size)
    new_size = tuple(int(sz / red_factor) for sz in bytes_image.size)
    reduced_photo = bytes_image.resize(new_size, Image.ANTIALIAS)
    photo_buffer = BytesIO()
    # reduced_photo.save(photo_buffer, format = 'PNG', optimize=True, quality=95)
    reduced_photo.save(photo_buffer, format = 'PNG')
    bytes_reduced_photo = photo_buffer.getvalue()
    b64str_reduced_photo = base64.b64encode(bytes_reduced_photo)
    return ('data:image/png;base64,' + b64str_reduced_photo.decode('ascii'))


def print_user_photo(filename) :
    """ Upload a user's avatar in the database """
    absolute_file_path = (environments[config_name]["api_app_path"] +
        "../../uploads/" + filename)

    with open(absolute_file_path, 'rb') as imagefile:
        base64string = base64.b64encode(imagefile.read()).decode('ascii')
        print(base64string)
        avatar_size = environments[config_name]["avatar_size"]
        lightened_image = lighten_image(base64string, avatar_size)

    print(lightened_image)  # print base64string to console
    # Will look something like:
    # iVBORw0KGgoAAAANS  ...  qQMAAAAASUVORK5CYII=

    # Save it into DB
    data = {"photo": lightened_image}
