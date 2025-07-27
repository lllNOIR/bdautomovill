from flask import Flask, render_template, request,redirect, url_for, flash
import pymysql


app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'

def connect_to_db():
    return pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='bd_automovilesv2',
    cursorclass=pymysql.cursors.DictCursor,
    ssl_disabled=True 
    )

@app.route("/")
def index():
    return render_template("registrar.html")

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nif = request.form['nif']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO clientes (nif, nombre, direccion, telefono) VALUES (%s,%s,%s,%s)",
                (nif, nombre, direccion, telefono)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('Cliente agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar cliente: {e}")
        return redirect(url_for('clientes'))

    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()  
        return render_template('registrar.html', clientes=clientes)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrar.html', clientes=[])

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nif = request.form['nif']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO clientes (nif, nombre, direccion, telefono) VALUES (%s,%s,%s,%s)",
                (nif, nombre, direccion, telefono)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('Cliente agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar cliente: {e}")
        return redirect(url_for('clientes'))

    # Consulta para mostrar la tabla
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()  
        return render_template('registrar.html', clientes=clientes)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrar.html', clientes=[])

@app.route('/elimina/<string:nif>', methods=['POST'])
def elimina(nif):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE nif=%s", (nif,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Cliente eliminado correctamente')
    except Exception as e:
        flash(f"Error al eliminar cliente: {e}")
    return redirect(url_for('clientes'))

@app.route('/edita/<nif>', methods=['GET', 'POST'])
def editaPAC(nif):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE nif=%s", (nif,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener cliente: {e}")
        return redirect(url_for('clientes'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute(
                "UPDATE clientes SET nombre=%s, direccion=%s, telefono=%s WHERE nif=%s",
                (nombre, direccion, telefono, nif)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash('Cliente actualizado correctamente')
            return redirect(url_for('clientes'))
        except Exception as e:
            flash(f"Error al actualizar cliente: {e}")
            return redirect(url_for('clientes'))
    return render_template('editarCLI.html', cliente=cliente)

@app.route('/coches', methods=['GET', 'POST'])
def coches():
    if request.method == 'POST':
        matricula = request.form['matricula']
        marca = request.form['marca']
        modelo = request.form['modelo']
        color = request.form['color']
        precio = request.form['precio']
        nif_cliente = request.form['nif_cliente']
        try:
            with connect_to_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO coches (matricula, marca, modelo, color, precio, nif_cliente) VALUES (%s,%s,%s,%s,%s,%s)",
                        (matricula, marca, modelo, color, precio, nif_cliente)
                    )
                    conn.commit()
            flash('Coche agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar coche: {e}")
        return redirect(url_for('registrarCOC'))
    try:
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM coches")
                coches = cursor.fetchall()
                cursor.execute("SELECT nif, nombre FROM clientes")
                clientes = cursor.fetchall()
        return render_template('registrarCOC.html', coches=coches, clientes=clientes)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarCOC.html', coches=[], clientes=[])

@app.route('/registrarCOC', methods=['GET', 'POST'])
def registrarCOC():
    if request.method == 'POST':
        matricula = request.form['matricula']
        marca = request.form['marca']
        modelo = request.form['modelo']
        color = request.form['color']
        precio = request.form['precio']
        nif_cliente = request.form['nif_cliente']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO coches (matricula, marca, modelo, color, precio, nif_cliente) VALUES (%s,%s,%s,%s,%s,%s)", (matricula, marca, modelo, color, precio, nif_cliente))
            conn.commit()
            cur.close()
            conn.close()
            flash('Coche agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar coche: {e}")
        return redirect(url_for('registrarCOC'))
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM coches")
            coches = cursor.fetchall()
            cursor.execute("SELECT nif, nombre FROM clientes")
            clientes = cursor.fetchall()
        return render_template('registrarCOC.html', coches=coches, clientes=clientes)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarCOC.html', coches=[], clientes=[])

@app.route('/elimina-matricula/<string:matricula>', methods=['POST'])
def eliminaCOC(matricula):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM coches WHERE matricula=%s", (matricula,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Coche eliminado correctamente')
    except Exception as e:
        flash(f"Error al eliminar coche: {e}")
    return redirect(url_for('registrarCOC'))

@app.route('/edita-coche/<string:matricula>', methods=['GET', 'POST'])
def editaCOC(matricula):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM coches WHERE matricula=%s", (matricula,))
        coche = cur.fetchone()
        cur.execute("SELECT nif, nombre FROM clientes")
        clientes = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener consultorio: {e}")
        return redirect(url_for('registrarCOC'))

    if request.method == 'POST':
        matricula = request.form['matricula']
        marca = request.form['marca']
        modelo = request.form['modelo']
        color = request.form['color']
        precio = request.form['precio']
        nif_cliente = request.form['nif_cliente']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE coches
                SET marca=%s, modelo=%s, color=%s, precio=%s, nif_cliente=%s
                WHERE matricula=%s
            """, (marca, modelo, color, precio, nif_cliente, matricula))
            conn.commit()
            cur.close()
            conn.close()
            flash('coche actualizado correctamente')
            return redirect(url_for('registrarCOC'))
        except Exception as e:
            flash(f"Error al actualizar consultorio: {e}")
            return redirect(url_for('registrarCOC'))
    return render_template('editarCOC.html', coche=coche, clientes=clientes)
   
@app.route('/medicos', methods=['GET', 'POST'])
def medicos():
    if request.method == 'POST':
        identificacion = request.form['MEDidentificacion']
        nombres = request.form['MEDnombres']
        apellidos = request.form['MEDapellidos']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO medicos (MEDidentificacion, MEDnombres, MEDapellidos) VALUES (%s,%s,%s)",
                        (identificacion, nombres, apellidos))
            conn.commit()
            cur.close()
            conn.close()
            flash('Médico agregado correctamente')
        except Exception as e:
            flash(f"Error al agregar médico: {e}")
        return redirect(url_for('registrarMED'))
    try:
        connection = connect_to_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM medicos")
            medicos = cursor.fetchall()
        return render_template('registrarMED.html', medicos=medicos)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarMED.html', medicos=[])

@app.route('/revisiones', methods=['GET', 'POST'])
def revisiones():
    if request.method == 'POST':
        matricula_coche = request.form['matricula_coche']
        filtro = request.form['filtro']
        aceite = request.form['aceite']
        frenos = request.form['frenos']
        try:
            with connect_to_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO revisiones (matricula_coche, filtro, aceite, frenos) VALUES (%s,%s,%s,%s)",
                        (matricula_coche, filtro, aceite, frenos)
                    )
                    conn.commit()
            flash('Revisión agregada correctamente')
        except Exception as e:
            flash(f"Error al agregar revisión: {e}")
        return redirect(url_for('revisiones'))
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT r.codigo, r.matricula_coche, c.marca, r.filtro, r.aceite, r.frenos
                    FROM revisiones r
                    JOIN coches c ON r.matricula_coche = c.matricula
                """)
                revisiones = cur.fetchall()
                cur.execute("SELECT matricula, marca FROM coches")
                coches = cur.fetchall()
        return render_template('registrarREV.html', revisiones=revisiones, coches=coches)
    except Exception as e:
        flash(f'Error al conectar a la base de datos: {e}', 'error')
        return render_template('registrarREV.html', revisiones=[], coches=[])

try:
    conn = connect_to_db()
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print("Error de conexión:", e)

if __name__ == '__main__':
    app.run(debug=True)


