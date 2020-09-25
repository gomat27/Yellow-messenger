from flask import jsonify


def ReturnInvalidData():
	return jsonify({"error_msg":"Invalid data"})


def ReturnKeyError():
	return jsonify({"error_msg":"Invalid Key in body"})


def ReturnValueError():
	return jsonify({"error_msg":"Invalid value in body"})


def ReturnUpdateError():
	return jsonify({"error_msg":"Unable to update data"})


def ReturnDuplicateDataError():
	return jsonify({"error_msg":"Data exits Aldready"})