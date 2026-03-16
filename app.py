from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "maxfiy_kalit_bu_yerda"

# Ma'lumotlar bazasini sozlash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ijara.db'
db = SQLAlchemy(app)

# Ijara ma'lumotlari uchun jadval
class Ijara(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uy_egasi = db.Column(db.String(100))
    manzil = db.Column(db.String(200))
    narxi = db.Column(db.String(50))
    tel = db.Column(db.String(20))

# Bazani yaratish
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    ijaralar = Ijara.query.all()
    return render_template('index.html', ijaralar=ijaralar)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "Mystra" and password == "mystra2014":
        session['admin'] = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    if session.get('admin'):
        yangi_ijara = Ijara(
            uy_egasi=request.form.get('uy_egasi'),
            manzil=request.form.get('manzil'),
            narxi=request.form.get('narxi'),
            tel=request.form.get('tel')
        )
        db.session.add(yangi_ijara)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    if session.get('admin'):
        ijara = Ijara.query.get(id)
        db.session.delete(ijara)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)