import functools
import os
import sys
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('ego', __name__, url_prefix='/ego')


@bp.route('/controller', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if request.form.get("forward"):
            print("forward pressed")
            return("nothing")
    return render_template('ego_ctrl/controller.html')

#background process happening without any refreshing
@bp.route('/background_process_test')
def background_process_test():
    print("hello sriram",file=sys.stdout)
    return ("nothing")