from datetime import datetime
from flask import jsonify, make_response, abort

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "Jones": {
        "fname": "Indiana",
        "lname": "Jones",
        "timestamp": get_timestamp(),
    },
    "Sparrow": {
        "fname": "Jack",
        "lname": " Sparrow",
        "timestamp": get_timestamp(),
    },
    "Snow": {
        "fname": "John",
        "lname": "Snow",
        "timestamp": get_timestamp(),
    },
}

def read_all():
    dict_clientes = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
    clientes = jsonify(dict_clientes)
    qtd = len(dict_clientes)
    content_range = "clientes 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    clientes.headers['Access-Control-Allow-Origin'] = '*'
    clientes.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    clientes.headers['Content-Range'] = content_range
    return clientes

def read_one(lname):
    if lname in PEOPLE:
        person = PEOPLE.get(lname)
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
        )
    return person


def create(person):
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{lname} criado com sucesso".format(lname=lname), 201
        )
    else:
        abort(
            406,
            "Pessoa com sobrenome {lname} ja existe".format(lname=lname),
        )


def update(lname, person):
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
        )

def delete(lname):
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} deletado com sucesso".format(lname=lname), 200
        )
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
        )

