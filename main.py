from flask import Flask, render_template, request
from apriori import impApriori
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def homepage():
    return render_template("page.html", title="HOME")

@app.route("/getResults", methods=["POST"])
def getResults():
    if request.method == "POST":
        inputFile = request.files["inputFile"]
        minSup = request.form["minSup"]

        if inputFile == "" or minSup == "":
            return render_template("page.html", title="HOME")

        resultData, timeTaken = impApriori(inputFile, float(minSup))
        
        return render_template("result.html", title="RESULTS", resultData = resultData, noOfItems = len(resultData), timeTaken = timeTaken)
    

if __name__ == "__main__":
    app.run(debug=True)
