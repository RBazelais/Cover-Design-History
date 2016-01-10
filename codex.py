from flask import Flask, jsonify, render_template, request
import airtable
import config
from collections import OrderedDict

app = Flask(__name__)
app.debug = True

at = airtable.Airtable(config.airtable_db_id, config.airtable_api_key)

def filter_dict(stack, fieldName, fieldValue):
    res = []
    for val in stack['records']:
        # print(val['fields'][fieldName])
        # print(val['fields'][fieldName].lower())

        if fieldName in val['fields']:
            if val['fields'][fieldName].lower().count(fieldValue.lower()) > 0:
                res.append(val)
    print(res)
    return res

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/autocomplete')
def autocomplete():

    term = request.args.get('term')
    print(term)

    results = at.get('Book Covers', sort_asc=True, sort_field='Cover Version')
    print(results)

    return jsonify(
            results=filter_dict(results, 'Cover Version', term)
    )


@app.route('/book/<id>')
def book(id):
    book = at.get('Books', id)
    return jsonify(book)


@app.route('/author/<id>')
def author(id):
    res = at.get('Authors', id)
    return jsonify(res)

@app.route('/cover/<id>')
def cover(id):
    res = at.get('Covers', id)
    return jsonify(res)

@app.route('/covers/<book_id>')
def covers(book_id):
    res = at.get('Covers')
    return jsonify(filter_dict(res, 'book', book_id))

if __name__ == '__main__':
    app.run()
