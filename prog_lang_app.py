from flask import Flask, request

app = Flask(__name__)

in_memory_datastore = {
    "COBOL": {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
    "ALGOL": {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
    "APL": {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
    "BASIC": {"name": "BASIC", "publication_year": 1964, "contribution": "runtime interpretation, office tooling"},
    "PL": {"name": "PL", "publication_year": 1966, "contribution": "constants, function overloading, pointers"},
    "SIMULA67": {"name": "SIMULA67", "publication_year": 1967,
                 "contribution": "class/object split, subclassing, protected attributes"},
    "PASCAL": {"name": "Pascal", "publication_year": 1970,
               "contribution": "modern unary, binary, and assignment operator syntax expectations"},
    "CLU": {"name": "CLU", "publication_year": 1975,
            "contribution": "iterators, abstract data types, generics, checked exceptions"},
}


@app.get('/programming_languages')
def list_programming_languages():
    before_year = request.args.get('before_year') or '3000'
    after_year = request.args.get('after_year') or '0'
    qualifying_data = list(
        filter(
            lambda pl: int(
                before_year) > pl['publication_year'] > int(after_year),
            in_memory_datastore.values()
        )
    )
    return {"programming_languages": qualifying_data}


def create_programming_language(new_lang):
    language_name = new_lang['name']
    new_lang['id'] = len(in_memory_datastore) + 1
    in_memory_datastore[language_name] = new_lang
    return new_lang


@app.route('/programming_languages/<nameX>', methods=['GET', 'PUT', 'POST'])
def programming_language_route(nameX):
    nameUpper = nameX.upper()
    if request.method == 'GET':
        return get_programming_language(nameUpper)
    elif request.method == 'POST':
        return create_programming_language(request.get_json(force=True))
    elif request.method == "PUT":
        return update_programming_language(nameUpper, request.get_json(force=True))


@app.route('/programming_languages/<name>')
def get_programming_language(name):
    return in_memory_datastore[name]


def update_programming_language(name, attributes):
    lang_attributes_updating = in_memory_datastore[name]
    lang_attributes_updating.update(attributes)
    return lang_attributes_updating
