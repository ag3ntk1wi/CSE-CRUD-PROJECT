import mysql.connector
import xml.etree.ElementTree as ET

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="malatecselec"
)

cursor = db.cursor()

root = ET.Element("database")

table_name = "student"
table_el = ET.SubElement(root, table_name)

cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]

for row in rows:
    record = ET.SubElement(table_el, "record")
    for col_name, value in zip(col_names, row):
        col = ET.SubElement(record, col_name)
        col.text = str(value) if value is not None else ""

# Save XML
tree = ET.ElementTree(root)
tree.write("student.xml", encoding="utf-8", xml_declaration=True)