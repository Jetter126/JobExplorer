from flask import Flask, render_template, request, redirect
import linkedin
import simplyhired
import csv
import pandas as pd

app = Flask(__name__)

# Home page
@app.route("/", methods=["POST", "GET"])
def index():
    # Check for method type
    if request.method == "POST":
        
        # Get values from occupation and city inputs
        occupation = request.form["occupation"]
        city = request.form["city"]

        # Ensure occupation is submitted
        if not occupation:
            return render_template("index.html", error="The occupation field is required", table=False)
        occupation.strip()

        # Ensure city is submitted
        if not city:
            return render_template("index.html", error="The city field is required", table=False)
        city.strip()

        # Clear previous data from CSV file
        with open("jobs.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Position", "Company", "Location", "Date Posted", "Salary", "Link"])

        # Load jobs into CSV file
        simplyhired.generate_jobs(occupation, city)
        linkedin.generate_jobs(occupation, city)

        with open("jobs.csv", "r") as file:
            reader = csv.reader(file)
            return render_template("index.html", error=0, table=reader)

    else:
        return render_template("index.html", error=0, table=False)

if __name__  == "__main__":
    app.run(debug=True)