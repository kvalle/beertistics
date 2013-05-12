import flask
import os.path
from beertistics import app, auth, user_service, visuals
from beertistics.exceptions import NoSuchUserException

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/show-user')
@auth.requires_auth
def show_user():
    username = flask.request.args.get('active-user', None)
    try:
        user = user_service.user_info_for(username)
        flask.session['shown_user'] = user
        flask.flash("Showing stats for %s (%s)." % (user['name'], user['username']), 'success')
    except NoSuchUserException:
        flask.flash("Found no user with username '%s'." % username, 'error')
    return flask.redirect(flask.url_for("index"))

@app.route('/test')
def test():
    return flask.render_template('test.html')

@app.route('/visual/<string:visual_id>')
@auth.requires_auth
def test(visual_id):
    visual = visuals.get_visual(visual_id)
    return flask.render_template(os.path.join('visuals', visual['template_name']))

@app.route('/photos')
@auth.requires_auth
def photos():
    return flask.render_template('photos.html')

@app.route('/map')
@auth.requires_auth
def map():
    return flask.render_template('map.html')

@app.route('/about')
@auth.requires_auth
def about():
    return flask.render_template('about.html')