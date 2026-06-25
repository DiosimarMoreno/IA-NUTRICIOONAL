from flask import Blueprint, render_template

evaluation_bp = Blueprint("evaluation", __name__)

@evaluation_bp.route("/evaluacion")
def evaluacion():
    return render_template("evaluacion.html")