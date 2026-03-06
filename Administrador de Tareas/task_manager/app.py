from flask import Flask, render_template, request, redirect, session, jsonify
from db import get_db_connection

app = Flask(__name__)
app.secret_key = "clave_secreta_123"


# =================== PÁGINA PRINCIPAL ===================
@app.route("/")
def index():
    return render_template("index.html")


# =================== REGISTRO ===================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
                (username, email, password)
            )

            conn.commit()

            cursor.close()
            conn.close()

            return redirect("/login")

        except Exception as e:
            return f"Error al registrar usuario: {e}"

    return render_template("register.html")


# =================== LOGIN ===================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, password)
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                session["user_id"] = user[0]
                return redirect("/dashboard")
            else:
                return "Usuario o contraseña incorrectos"

        except Exception as e:
            return f"Error en login: {e}"

    return render_template("login.html")


# =================== DASHBOARD ===================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# =================== VER TAREAS ===================
@app.route("/tasks")
def tasks():

    if "user_id" not in session:
        return redirect("/login")

    try:

        user_id = session["user_id"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE user_id=%s",
            (user_id,)
        )

        tasks = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("tasks.html", tasks=tasks)

    except Exception as e:
        return f"Error al obtener tareas: {e}"


# =================== AGREGAR TAREA ===================
@app.route("/add_task", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["description"]

    try:

        user_id = session["user_id"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (title, description, user_id) VALUES (%s,%s,%s)",
            (title, description, user_id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/tasks")

    except Exception as e:
        return f"Error al agregar tarea: {e}"


# =================== ELIMINAR TAREA ===================
@app.route("/delete_task/<int:id>")
def delete_task(id):

    if "user_id" not in session:
        return redirect("/login")

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id=%s",
            (id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/tasks")

    except Exception as e:
        return f"Error al eliminar tarea: {e}"


# =================== EDITAR TAREA ===================
@app.route("/edit_task/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        cursor.execute(
            "UPDATE tasks SET title=%s, description=%s WHERE id=%s",
            (title, description, id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/tasks")

    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_task.html", task=task)


# =================== LOGOUT ===================
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")


# =================== API REST ===================

# Obtener tareas
@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(tasks)


# Crear tarea
@app.route("/api/tasks", methods=["POST"])
def api_create_task():

    data = request.json

    title = data["title"]
    description = data["description"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (%s,%s)",
        (title, description)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Tarea creada correctamente"})


# Actualizar tarea
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def api_update_task(id):

    data = request.json

    title = data["title"]
    description = data["description"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET title=%s, description=%s WHERE id=%s",
        (title, description, id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Tarea actualizada"})


# Eliminar tarea
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def api_delete_task(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Tarea eliminada"})


# =================== INICIAR SERVIDOR ===================
if __name__ == "__main__":
    app.run(debug=True)