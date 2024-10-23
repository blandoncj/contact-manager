import sqlite3 as sql
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask import Flask, flash, redirect, render_template, request, url_for
from entity.user import UserEntity
from entity.contact import ContactEntity
from controllers.auth_controller import AuthController
from controllers.contact_controller import ContactController
from dto.login_dto import LoginDTO
from exception.user_exceptions import (
    InvalidCredentialsException,
    NicknameAlreadyExistsException,
)

app = Flask(__name__)
app.secret_key = "secret_key"

login_manager_app = LoginManager(app)

auth_controller = AuthController()
contact_controller = ContactController()


@login_manager_app.user_loader
def load_user(user_id: int):
    return auth_controller.find_by_id(user_id)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]

        if not nickname or not password:
            flash("All fields are required", "error")
            return redirect(url_for("index"))

        user = LoginDTO(nickname, password)

        try:
            logged_user = auth_controller.login(user)
            if logged_user:
                login_user(logged_user)
                return redirect(url_for("contacts"))
        except (sql.Error, InvalidCredentialsException) as e:
            flash(str(e), "error")
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        nickname = request.form["nickname"]
        password = request.form["password"]
        passoword2 = request.form["password2"]

        if not name or not nickname or not password or not passoword2:
            flash("All fields are required", "error")
            return redirect(url_for("register"))

        if password != passoword2:
            flash("Passwords don't match", "error")
            return redirect(url_for("register"))

        user = UserEntity(None, name, nickname, password)

        try:
            auth_controller.register(user)
            logged_user = auth_controller.login(LoginDTO(nickname, password))
            if logged_user:
                login_user(logged_user)
                flash("Account created successfully", "success")
                return redirect(url_for("contacts"))
        except (sql.Error, NicknameAlreadyExistsException) as e:
            flash(str(e), "error")
            return redirect(url_for("register"))

    return render_template("signup.html")


@app.route("/contacts")
@login_required
def contacts():
    user_id = current_user.id
    contacts = contact_controller.list_all_contacts(user_id)
    if len(contacts) == 0:
        flash("No contacts found", "error")
    return render_template("contacts.html", contacts=contacts)


@app.route("/search-contacts", methods=["GET"])
@login_required
def search_contacts():
    query = request.args.get("query")
    user_id = current_user.id
    contacts = contact_controller.list_contacts_by_query(query, user_id)
    if len(contacts) == 0:
        flash("No contacts found", "error")
    return render_template("contacts.html", contacts=contacts)


@app.route("/add-contact", methods=["GET", "POST"])
@login_required
def add_contact():
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        category = request.form.get("category")
        address = request.form["address"]
        email = request.form["email"]
        is_favorite = request.form.get("favorite", "0")
        is_favorite = 1 if is_favorite == "1" else 0
        phones = [request.form["phone"]]
        other_phone = request.form["other_phone"]

        if not name or not category or not phones:
            flash("All fields are required", "error")
            return redirect(url_for("add_contact"))

        if other_phone:
            phones.append(other_phone)

        user_id = current_user.id

        contact = ContactEntity(
            None, name, lastname, phones, category, address, email, is_favorite
        )

        try:
            contact_controller.create_contact(contact, user_id)
            flash("Contact created successfully", "success")
            return redirect(url_for("contacts"))
        except sql.Error as e:
            flash(str(e), "error")
            return redirect(url_for("add_contact"))
    return render_template("add_contact.html")


@app.route("/update-contact/<int:contact_id>", methods=["GET", "POST"])
@login_required
def update_contact(contact_id: int):
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        category = request.form.get("category")
        address = request.form["address"]
        email = request.form["email"]
        is_favorite = request.form.get("favorite", "0")
        is_favorite = 1 if is_favorite == "1" else 0
        phones = [request.form["phone"]]
        other_phone = request.form["other_phone"]

        if not name or not category or not phones:
            flash("All fields are required", "error")
            return redirect(url_for("add_contact"))

        if other_phone:
            phones.append(other_phone)

        contact = ContactEntity(
            contact_id, name, lastname, phones, category, address, email, is_favorite
        )

        try:
            contact_controller.update_contact(contact)
            flash("Contact updated successfully", "success")
            return redirect(url_for("contacts"))
        except sql.Error as e:
            flash(str(e), "error")
            return redirect(url_for("update_contact", id=contact_id))

    contact = contact_controller.find_contact_by_id(contact_id)
    return render_template("update_contact.html", contact=contact)


@app.route("/delete-contact", methods=["POST"])
@login_required
def delete_contact():
    if request.method == "POST":
        contact_id = request.form["contact_id"]

        try:
            contact_controller.delete_contact(contact_id)
            flash("Contact deleted successfully", "success")
            return redirect(url_for("contacts"))
        except sql.Error as e:
            flash(str(e), "error")
            return redirect(url_for("contacts"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
