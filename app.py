import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from database import init_db, get_db
from recommendation import recommend_license

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key-before-deployment"

init_db()

LICENSES = {
    "MIT": {
        "name": "MIT License",
        "short": "A short, permissive license that allows reuse with minimal conditions.",
        "description": "The MIT License allows people to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software.",
        "permissions": ["Commercial use", "Modification", "Distribution", "Private use"],
        "conditions": ["Include the copyright notice", "Include the license text"],
        "restrictions": ["The software is provided without warranty", "The authors are not liable"],
        "commercial": "Yes",
        "modification": "Yes",
        "distribution": "Yes",
        "attribution": "Yes — preserve copyright and license notices",
        "copyleft": "No",
        "patent": "No explicit patent grant",
        "advantages": ["Very simple and short", "Allows proprietary derivatives", "Widely recognized"],
        "disadvantages": ["No explicit patent license", "Does not require modified versions to remain open source"],
        "url": "https://opensource.org/license/mit"
    },
    "GPL": {
        "name": "GNU General Public License (GPL)",
        "short": "A copyleft license that requires distributed derivative works to remain under the GPL.",
        "description": "The GNU GPL grants broad rights to use, study, modify, and distribute software. When covered modified versions are distributed, the applicable GPL terms require source-code availability and licensing under the GPL.",
        "permissions": ["Commercial use", "Modification", "Distribution", "Private use"],
        "conditions": ["Provide corresponding source when distributing covered binaries", "Preserve copyright and license notices", "License covered derivative works under the GPL", "State significant changes"],
        "restrictions": ["No additional restrictions that take away granted freedoms", "Copyleft obligations apply to covered derivative works when distributed"],
        "commercial": "Yes",
        "modification": "Yes",
        "distribution": "Yes",
        "attribution": "Yes — preserve notices and provide license information",
        "copyleft": "Yes",
        "patent": "Yes — GPLv3 includes an express contributor patent license, subject to its terms",
        "advantages": ["Protects recipients' freedoms", "Ensures covered distributed derivatives remain under the same license family", "GPLv3 includes patent provisions"],
        "disadvantages": ["Copyleft obligations may not suit every project", "Compliance can require source-code and notice processes"],
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html"
    },
    "Apache": {
        "name": "Apache License 2.0",
        "short": "A permissive license with an express patent license and patent-termination provision.",
        "description": "Apache License 2.0 permits use, modification, distribution, and commercial use. It includes an express patent license from contributors and requires preservation of notices and handling of any NOTICE file.",
        "permissions": ["Commercial use", "Modification", "Distribution", "Private use", "Patent use under the license grant"],
        "conditions": ["Include a copy of the license", "Mark modified files", "Retain relevant copyright, patent, trademark, and attribution notices", "Reproduce applicable NOTICE content"],
        "restrictions": ["No trademark rights are granted", "Patent litigation against a contributor can terminate the patent license"],
        "commercial": "Yes",
        "modification": "Yes",
        "distribution": "Yes",
        "attribution": "Yes — preserve notices and applicable NOTICE content",
        "copyleft": "No",
        "patent": "Yes — express contributor patent grant",
        "advantages": ["Explicit patent grant", "Permissive commercial reuse", "Clear notice and modification requirements"],
        "disadvantages": ["Longer and more detailed than MIT/BSD", "NOTICE and patent provisions need attention"],
        "url": "https://www.apache.org/licenses/LICENSE-2.0"
    },
    "BSD": {
        "name": "BSD 3-Clause License",
        "short": "A permissive license with notice requirements and a non-endorsement clause.",
        "description": "The BSD 3-Clause License permits redistribution and use in source and binary forms, with or without modification, provided its conditions are followed.",
        "permissions": ["Commercial use", "Modification", "Distribution", "Private use"],
        "conditions": ["Retain copyright notice, conditions, and disclaimer in source distributions", "Reproduce them in binary documentation or materials"],
        "restrictions": ["Cannot use copyright holder or contributor names to endorse products without permission"],
        "commercial": "Yes",
        "modification": "Yes",
        "distribution": "Yes",
        "attribution": "Yes — preserve notices and disclaimer",
        "copyleft": "No",
        "patent": "No explicit patent grant in the standard 3-Clause text",
        "advantages": ["Permissive and business-friendly", "Allows proprietary derivatives", "Clear redistribution conditions"],
        "disadvantages": ["No explicit patent grant in standard text", "Requires notice preservation"],
        "url": "https://opensource.org/license/bsd-3-clause"
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/licenses")
def licenses():
    return render_template("licenses.html", licenses=LICENSES)

@app.route("/licenses/<key>")
def license_detail(key):
    item = LICENSES.get(key)
    if not item:
        abort(404)
    return render_template("license_detail.html", key=key, item=item)

@app.route("/comparison")
def comparison():
    return render_template("comparison.html", licenses=LICENSES)

@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    if request.method == "GET":
        return render_template("recommendation.html")
    data = {
        "project_name": request.form.get("project_name", "").strip(),
        "commercial": request.form.get("commercial", ""),
        "modification": request.form.get("modification", ""),
        "redistribution": request.form.get("redistribution", ""),
        "same_license": request.form.get("same_license", ""),
        "attribution": request.form.get("attribution", ""),
        "patent": request.form.get("patent", ""),
        "preference": request.form.get("preference", "")
    }
    if not data["project_name"] or len(data["project_name"]) > 100:
        flash("Enter a project name (1–100 characters).", "danger")
        return render_template("recommendation.html", form_data=data), 400
    allowed = {
        "commercial": {"yes", "no"},
        "modification": {"yes", "no"},
        "redistribution": {"yes", "no"},
        "same_license": {"yes", "no", "not_sure"},
        "attribution": {"yes", "no"},
        "patent": {"yes", "no"},
        "preference": {"permissive", "copyleft", "no_preference"}
    }
    for field, values in allowed.items():
        if data[field] not in values:
            flash("Please answer every question using the provided options.", "danger")
            return render_template("recommendation.html", form_data=data), 400

    result = recommend_license(data)
    db = get_db()
    cursor = db.execute("""
        INSERT INTO recommendations
        (project_name, requirements_json, recommended_key, explanation, alternatives, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["project_name"], json.dumps(data), result["recommended_key"],
        result["explanation"], json.dumps(result["alternatives"]),
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    db.commit()
    recommendation_id = cursor.lastrowid
    return render_template("result.html", result=result, licenses=LICENSES,
                           project_name=data["project_name"], recommendation_id=recommendation_id)

@app.route("/history")
def history():
    db = get_db()
    rows = db.execute("SELECT * FROM recommendations ORDER BY id DESC").fetchall()
    return render_template("history.html", rows=rows)

@app.route("/history/<int:record_id>")
def history_detail(record_id):
    row = get_db().execute("SELECT * FROM recommendations WHERE id=?", (record_id,)).fetchone()
    if not row:
        abort(404)
    result = recommend_license(json.loads(row["requirements_json"]))
    return render_template("result.html", result=result, licenses=LICENSES,
                           project_name=row["project_name"], recommendation_id=record_id,
                           from_history=True)

@app.post("/history/<int:record_id>/delete")
def delete_history(record_id):
    db = get_db()
    db.execute("DELETE FROM recommendations WHERE id=?", (record_id,))
    db.commit()
    flash("Recommendation record deleted.", "success")
    return redirect(url_for("history"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or len(name) > 80 or not email or "@" not in email or len(email) > 120 or not message or len(message) > 2000:
            flash("Please provide a valid name, email address, and message (maximum 2,000 characters).", "danger")
            return render_template("contact.html"), 400
        db = get_db()
        db.execute("INSERT INTO contact_messages (name,email,message,created_at) VALUES (?,?,?,?)",
                   (name, email, message, datetime.now().strftime("%Y-%m-%d %H:%M")))
        db.commit()
        flash("Thank you! Your message has been saved.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
