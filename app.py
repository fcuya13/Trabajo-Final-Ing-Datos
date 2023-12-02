from flask import Flask, render_template, request, redirect,url_for
from datetime import datetime
import cx_Oracle
from collections.abc import MutableSequence

app = Flask(__name__)

username = ""
password = ""
host = ''
connection_str = f"{username}/{password}@{host}"

try:
    conn = cx_Oracle.connect(connection_str)
except cx_Oracle.Error as err:
    print (f"Error de conexión {err}")


def consultar_tabla(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        conn.commit()
        return {"Data": results}
    except Exception as e:
        return {"error": str(e)}

def insertar_tabla(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    query = "SELECT c.id, c.nombre, e.mail, cc.celular, d.descripcion FROM cliente c JOIN direccion d ON c.id = d.id_cliente JOIN email e ON c.id = e.id_cliente JOIN celular_cliente cc on c.id = cc.id_cliente ORDER BY c.id"
    data = consultar_tabla(query)
    print(data)
    return render_template('clientes.html', resultados = data)

@app.route('/ventas')
def ventas():
    query = "SELECT v.fecha, c.nombre as Cliente, p.nombre as Producto, v.cant, p.preciou, v.precio_t, d.descripcion, e.costo FROM venta v JOIN producto p on p.id = v.id_prod JOIN cliente c on c.id = v.id_cliente JOIN envio e on e.id_venta = v.id JOIN direccion d on d.id = e.id_direccion ORDER BY v.fecha DESC"
    data = consultar_tabla(query)
    print(data)
    return render_template('ventas.html', resultados = data)

@app.route('/envios')
def envios():
    query = "SELECT e.fecha, c.nombre, d.descripcion, p.nombre, e.estado FROM envio e JOIN venta v on v.id = e.id_venta JOIN cliente c on v.id_cliente = c.id JOIN direccion d on d.id = e.id_direccion JOIN producto p on p.id = v.id_prod ORDER BY e.fecha desc"
    data = consultar_tabla(query)
    print(data)
    return render_template('envios.html', resultados=data)

@app.route('/addc', methods=['GET','POST'])
def procesar_formulario():
    if request.method == "POST":
        try:
            dni_ruc = int(request.form['dni_ruc'])
            nombre = request.form['nombre']
            correo = request.form['correo']
            celular = int(request.form['celular'])
            direccion = request.form['direccion']
            ciudad = request.form['ciudad']
            distrito = request.form['distrito']
            codigo_postal = int(request.form['cod_postal'])
            with conn.cursor() as cursor:
                cursor.callproc('agregar_cliente', [dni_ruc, nombre, correo, direccion, ciudad, distrito, codigo_postal, celular])
                conn.commit()
            return redirect(url_for('clientes'))
        except Exception as e:
            print(e)
            return render_template("/addcliente.html")
    return render_template("/addcliente.html")

@app.route('/addventa', methods=['GET', 'POST'])
def formulario_venta():
    if request.method == "POST":
        try:
            producto_id = int(request.form['producto'])
            direccion_id = int(request.form['direccion'])
            cliente_id = int(request.form['cliente'])
            cantidad = int(request.form['cantidad'])
            costo = int(request.form['envio'])
            now = datetime.now()
            fecha = now.strftime("%Y-%m-%d")
            print((producto_id, direccion_id, cliente_id,cantidad,costo,fecha))
            with conn.cursor() as cursor:
                cursor.callproc('realizar_venta', [fecha, direccion_id, cantidad, cliente_id, producto_id, costo])
                conn.commit()
            return redirect(url_for('ventas'))
        except Exception as e:
            print(e)
            return redirect(url_for('formulario_venta'))

    productos = consultar_tabla("SELECT * FROM producto")['Data']
    clientes = consultar_tabla("SELECT * FROM cliente")['Data']
    direcciones = consultar_tabla("SELECT id, descripcion, id_cliente from Direccion")['Data']
    return render_template("addventa.html", productos=productos, clientes=clientes, direcciones=direcciones)


if __name__ == '__main__':
    app.run(debug=True)
