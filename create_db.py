import pymysql

# --- Configuración para la conexión inicial a MySQL ---
DB_USER = "root"
DB_PASSWORD = ""  # Vacío por defecto en XAMPP
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "testdb"

try:
    # Nos conectamos al servidor MySQL (sin especificar la base de datos aún)
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Conexión exitosa al servidor MySQL.")

    with connection.cursor() as cursor:
        # Creamos la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        print(f"Base de datos '{DB_NAME}' creada o ya existente.")

except pymysql.MySQLError as e:
    print(f"Error al conectar o crear la base de datos: {e}")

finally:
    if 'connection' in locals() and connection.open:
        connection.close()
        print("Conexión cerrada.")

