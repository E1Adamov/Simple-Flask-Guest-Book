#!/usr/bin/python3

from contextlib import contextmanager
import flask
import dataset

from tests import helpers
import config

app = flask.Flask(__name__)


@contextmanager
def db_table(data_base: str = config.DB,
             table_name: str = config.URL_BOARD) -> dataset.Table:
    """
    Had to implement this because Flask starts a new thread for each request, while cursors created in one thread,
    can only be used in the same one. Probably, 6 years ago, this app used to work the way is was created initially,
    but now it doesn't.
    :param data_base: database you want to work with
    :param table_name: name of the table you want to work with
    :return: dataset.Table object
    """
    with database(data_base) as db:
        yield db[table_name]


@contextmanager
def database(data_base: str) -> dataset.Database:
    """
    :param data_base: database you want to work with
    :return: dataset.Database object
    """
    with dataset.connect(data_base) as db:
        yield db


@app.route(f'/{config.URL_POST_MSG}', methods=['GET'])
def render_post_message():
    return flask.render_template('post_message.html')


@app.route(f'/{config.URL_BOARD}', methods=['GET'])
def render_message_board():
    with db_table() as table:
        signatures = table.find()
        return flask.render_template('message_board.html', signatures=signatures)


@app.route(f'/{config.URL_SUBMIT}', methods=['POST'])
def submit_message():
    post = dict(name=flask.request.form['name'], message=flask.request.form['message'])

    if not helpers.is_valid_message(post['message']):
        flask.abort(403, 'Message can not contain substring "RED"')

    with db_table() as table:
        table.insert(post)
        return flask.redirect(flask.url_for('render_message_board'))


@app.route('/<path:filename>.js', methods=['GET'])
def send_js(filename):
    filename = filename + '.js'
    return flask.send_from_directory(directory=config.PATH_JS, filename=filename)


def main():
    # with db_table() as table:  # TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! delete this !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #     table.drop()

    app.run(debug=True)


if __name__ == '__main__':
    main()

