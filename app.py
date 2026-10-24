from flask import Flask, render_template, request, redirect, url_for
from decimal import Decimal
import pyodbc

app = Flask(__name__)

CADENA = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=DESKTOP-HUL0GQC\SQLEXPRESS;"
    r"DATABASE=GestionGastos;"
    r"Trusted_Connection=yes;"
    r"TrustServerCertificate=yes;"
)


def obtener_conexion():
    return pyodbc.connect(CADENA)


@app.route("/")
def inicio():
    return "Hola mundo, esta es mi app de gastos"


@app.route("/categorias")
def categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT ID_Categoria, NombreCategoria FROM TablaCategoria ORDER BY ID_Categoria"
    )
    lista = cursor.fetchall()
    conexion.close()
    return render_template("categorias.html", categorias=lista)



@app.route("/gastos/nuevo", methods=["GET", "POST"])
def nuevo_gasto():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":
        descripcion = request.form["descripcion"]
        monto = Decimal(request.form["monto"])
        fecha = request.form["fecha"]
        id_categoria = int(request.form["categoria"])

        # Como no usamos IDENTITY, calculamos el próximo ID a mano
        cursor.execute("SELECT ISNULL(MAX(ID_Gasto), 0) + 1 FROM TablaGasto")
        nuevo_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO TablaGasto "
            "(ID_Gasto, Descripcion, Monto, FechaGasto, ID_Categoria) "
            "VALUES (?, ?, ?, ?, ?)",
            nuevo_id, descripcion, monto, fecha, id_categoria,
        )
        conexion.commit()
        conexion.close()
        return redirect(url_for("lista_gastos"))

    # Si llegó por GET, mostramos el formulario con las categorías
    cursor.execute(
        "SELECT ID_Categoria, NombreCategoria FROM TablaCategoria ORDER BY NombreCategoria"
    )
    lista = cursor.fetchall()
    conexion.close()
    return render_template("nuevo_gasto.html", categorias=lista)


@app.route("/gastos")
def lista_gastos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT g.ID_Gasto, g.Descripcion, g.Monto, g.FechaGasto, c.NombreCategoria "
        "FROM TablaGasto g "
        "JOIN TablaCategoria c ON g.ID_Categoria = c.ID_Categoria "
        "ORDER BY g.FechaGasto DESC, g.ID_Gasto DESC"
    )
    lista = cursor.fetchall()
    conexion.close()
    return render_template("gastos.html", gastos=lista)

if __name__ == "__main__":
    app.run(debug=True)
