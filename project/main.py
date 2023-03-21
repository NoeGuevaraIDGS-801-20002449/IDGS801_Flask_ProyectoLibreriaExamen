from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . models import Libro
from . import db

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/profile')
@login_required
def profile():
    libros = Libro.query.all()
    return render_template('profile.html', name = current_user.name, libros = libros)

@main.route('/admin')
@login_required
@roles_required('admin')
def admin():
    libros = Libro.query.all()
    return render_template('admin.html', libros = libros)

@main.route('/insertLibro', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def insert_libro():
  if request.method == 'POST':
    libros = Libro (
        name = request.form.get('nombre'),
        author = request.form.get('autor'),
        tomo = request.form.get('tomo'),
        price = request.form.get('precio'),
        exist = request.form.get('estatus')
    )
            
    db.session.add(libros)
    db.session.commit()
    flash("Libro agregado correctamente!")
    return redirect(url_for('main.admin'))
  return render_template('insert_Libro.html')

@main.route('/updateLibro', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def update_libro():
    if request.method == 'GET':
        id = request.args.get('id')
        libros = db.session.query(Libro).filter(Libro.id == id).first()

        nombre = request.form.get('nombre', libros.name)
        autor = request.form.get('autor', libros.author)
        tomo = request.form.get('tomo', libros.tomo)
        precio = request.form.get('precio', libros.price)
        estatus = request.form.get('estatus', libros.exist)
        return render_template('update_Libro.html', id = id, nombre = nombre, autor = autor, tomo = tomo, precio = precio, estatus = estatus)
    
    if request.method == 'POST':
        id = request.form.get('id')
        libros = db.session.query(Libro).filter(Libro.id == id).first()

        libros.name = request.form.get('nombre')
        libros.author = request.form.get('autor')
        libros.tomo = request.form.get('tomo')
        libros.price = request.form.get('precio')
        libros.exist = request.form.get('estatus')

        db.session.add(libros)
        db.session.commit()
        flash("Libro actualizado correctamente!")
        return redirect(url_for('main.admin'))
    return render_template('update_Libro.html')

@main.route('/deleteLibro', methods = ['GET'])
@login_required
@roles_required('admin')
def delete_manga():
   id = request.args.get('id')
   alumno = db.session.query(Libro).filter(Libro.id == id).first()

   db.session.delete(alumno)
   db.session.commit()
   flash("Libro eliminado correctamente!")
   return redirect(url_for('main.admin'))