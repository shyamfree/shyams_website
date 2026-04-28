from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"   # change later

# ===== MAIN PAGES =====

@app.route("/")
def dashboard():
    if not is_logged_in():
        return redirect("/login")
    return render_template("dashboard.html", request=request, tools=get_tools())

@app.route("/resume")
def resume():
    if not is_logged_in():
        return redirect("/login")
    return render_template("resume.html", request=request, tools=get_tools())

@app.route("/settings")
def settings():
    if not is_logged_in():
        return redirect("/login")
    return render_template("settings.html", request=request, tools=get_tools())

@app.route("/skills/devops")
def devops():
    if not is_logged_in():
        return redirect("/login")
    return render_template("devops.html", request=request, tools=get_tools())


# ===== DYNAMIC TOOL ROUTE =====

@app.route("/skills/devops/<tool>", methods=["GET", "POST"])
def tool_page(tool):
    if not is_logged_in():
        return redirect("/login")

    section = request.args.get("section", "overview")
    file_path = f"data/{tool}.json"

    if not os.path.exists(file_path):
        return "Tool not found", 404

    with open(file_path) as f:
        data = json.load(f)

    # 🔥 SAVE UPDATED CONTENT
    if request.method == "POST" and session.get("user") == "admin":
        new_content = request.form.get("content")

        data["sections"][section] = new_content

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        return redirect(f"/skills/devops/{tool}?section={section}")

    return render_template(
        "tool.html",
        tool_name=data.get("name"),
        tool_desc=data.get("description"),
        sections=data.get("sections", {}),
        section=section,
        tool=tool,
        request=request,
        tools=get_tools()
    )

def get_tools():
    tools = []

    for file in os.listdir("data"):
        if file.endswith(".json"):
            with open(f"data/{file}") as f:
                data = json.load(f)

                tools.append({
                    "name": data.get("name"),
                    "slug": file.replace(".json", "")
                })

    return tools

# ===== Login =====

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # simple admin check
        if username == "admin" and password == "admin123":
            session["user"] = "admin"
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


# ===== Logout =====
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

def is_logged_in():
    return "user" in session
# ===== RUN APP =====

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)