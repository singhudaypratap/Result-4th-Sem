from flask import Flask, request, render_template_string
import pandas as pd

# Load file
file_path = "Result Analysis of B.Tech. IV Sem 2024-25.xlsx"
branches = ['CS', 'CSR-D', 'AI&DS-E', 'CS(AI)-F', 'CS(DS)-G', 'CS(IOT)-H']
dfs = {b: pd.read_excel(file_path, sheet_name=b, skiprows=10) for b in branches}

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Result Lookup</title>
</head>
<body>
    <h2>Student Result Lookup</h2>
    <form method="POST">
        Registration No: <input type="text" name="reg"><br><br>
        Branch: 
        <select name="branch">
            {% for b in branches %}
            <option value="{{b}}">{{b}}</option>
            {% endfor %}
        </select><br><br>
        <input type="submit" value="Get Result">
    </form>

    {% if result is not none %}
        <h3>Result</h3>
        {{ result|safe }}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        reg = request.form["reg"].strip()
        branch = request.form["branch"]
        df = dfs[branch]

        # Match by registration number (assuming 2nd column is Registration Number)
        match = df[df.iloc[:, 2] == reg]

        if not match.empty:
            result = match.to_html(index=False)
        else:
            result = "<p>No record found.</p>"

    return render_template_string(HTML_TEMPLATE, branches=branches, result=result)

if __name__ == "__main__":
    app.run(debug=True)
