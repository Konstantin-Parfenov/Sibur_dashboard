from flask import abort, Blueprint, current_app, flash, render_template, redirect, request, url_for



blueprint = Blueprint('index', __name__)

@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('dashboard.html')