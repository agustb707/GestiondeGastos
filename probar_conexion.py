import pyodbc

cadena = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=DESKTOP-HUL0GQC\SQLEXPRESS;"
    r"DATABASE=GestionGastos;"
    r"Trusted_Connection=yes;"
    r"TrustServerCertificate=yes;"
)

conexion = pyodbc.connect(cadena)
cursor = conexion.cursor()

cursor.execute("SELECT ID_Categoria, NombreCategoria FROM TablaCategoria")
for fila in cursor.fetchall():
    print(fila.ID_Categoria, fila.NombreCategoria)

conexion.close()