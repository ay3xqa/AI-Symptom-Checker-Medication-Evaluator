from flask import Flask, render_template, request, url_for, jsonify
import ml
import disease

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/disEval')
def disEval():
    return render_template("diseaseEvaluation.html")

# @app.route('/drugs')
# def adder_page():
#     errors = ""
#     if request.method == "POST":
#         print("asdfdf")
#         disease = None
#         try:
#             age = str(request.form["age"])
#             gender = str(request.form["gender"])
#             disease = str(request.form["disease"])
#             symptoms = str(request.form["smp"])
#             print("HI")
#         except:
#             errors += "<p>{!r} is not a disease.</p>\n".format(request.form["disease"])
#     else:
#         return '''
#
#         '''


@app.route('/calculateprob', methods = ["GET","POST"])
def calculateprob():
    if request.method == "POST":
        new_freq = request.get_json()
        toInput = new_freq["newfreq"]
        initial = ml.main(toInput)
        return jsonify(total = initial)

@app.route('/rankDrugs', methods = ["GET","POST"])
def rankDrugs():
    if request.method == "POST":
        new_freq = request.get_json()
        toInput = new_freq["newfreq"]
        difinitial = disease.main(toInput)
        print(difinitial)
        return jsonify(atotal=difinitial)

@app.route('/drugEval')
def drugEval():
    return render_template("drugEvaluation.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()


