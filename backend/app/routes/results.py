from flask import Blueprint, render_template

results_bp = Blueprint("results", __name__)

@results_bp.route("/resultados")
def resultados():
    return render_template("resultados.html")