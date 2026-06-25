from flask import Blueprint, render_template

account_bp = Blueprint("account", __name__)

@account_bp.route("/cuenta")
def cuenta():
    return render_template("cuenta.html")