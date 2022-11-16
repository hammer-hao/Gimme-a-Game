from flask import Flask, render_template, redirect, url_for
import os
from oauthlib.oauth2 import WebApplicationClient
import requests
import dotenv

BATTLENET_CLIENT_ID= '728eadaf977a414a91ceed3ee1bc07d8'
BATTLENET_CLIENT_SECRET= 'xt5RjcvTARLvJ5A6bg6wyufU8Ni5VM4r''
secret_key= "b'6\x910\xca_\xf5\x9d3\xc6\xf74\xdbet\x9e\x0f'"

app = Flask(__name__)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'
if __name__=="__main__":
    app.run(debug=True)