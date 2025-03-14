from flask import Blueprint, request, jsonify, json

blueprint = Blueprint("nfc_chip", __name__)

default_redirect = "divi.votisek.dev/edit-redirect"

@blueprint.route("/get-redirect/<redirect_id>", methods=['GET', 'POST'])
def get_redirect(redirect_id):
    if request.method == "GET":
        with open("users.json", "r+") as f:
            users = dict(json.load(f))
            if redirect_id in users.keys():
                users[redirect_id][count] += 1
                json.dump(users, f)
                f.close()
                return jsonify(users[redirect_id]), 200
            else:<
                f.close()
                return jsonify("{}"), 400

@blueprint.route("/edit-redirect", methods=['GET'])
def edit_redirect():
    redirect_id = request.args.get("redirect_id")
    url = request.args.get("url")
    with open("users.json", "r+") as f:
        users = dict(json.load(f))
        if redirect_id in users.keys():


@blueprint.route("/new-chip", methods=['GET'])
def add_chip():
    redirect_id = request.args.get("redirect_id")
    color = request.args.get("color")
    with open("endpoints/nfc_chip/users.json", "r+") as f:
        users = dict(json.load(f))
        users.update({
            redirect_id: {
                "redirect": default_redirect,
                "color": color,
                "redirect_count": 0
            }
})
        