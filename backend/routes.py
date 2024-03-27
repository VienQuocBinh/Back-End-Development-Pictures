from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.json:
        abort(400)
    picture = {
        "id": data[-1]["id"] + 1 if data else 1,
        "pic_url": request.json["pic_url"],
        "event_country": request.json["event_country"],
        "event_state": request.json["event_state"],
        "event_city": request.json["event_city"],
        "event_date": request.json["event_date"]
    }
    # Check for duplicate picture
    if any(item["pic_url"] == picture["pic_url"] for item in data):
        return jsonify({"message": f"picture with id {picture['id']} already present"}), 302
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        abort(404)
    if not request.json:
        abort(400)
    picture.update(request.json)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        abort(404)
    data.remove(picture)
    return jsonify({"message": "Picture deleted successfully"}), 204
