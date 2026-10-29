import csv
import io

import openpyxl


def test_soa_export_xlsx_endpoint(client):
    # Act
    response = client.get("/soa/export/xlsx")

    # Assert HTTP headers
    assert response.status_code == 200
    assert "application/vnd.openxmlformats" in response.headers["content-type"]
    assert "Declaracion_de_Aplicabilidad" in response.headers["content-disposition"]

    # Assert content is valid Excel file
    wb = openpyxl.load_workbook(io.BytesIO(response.content))
    ws = wb.active
    assert ws.title == "Declaración de Aplicabilidad"

    # Row 1 is Title, Row 2 is Subtitle, Row 4 is Headers, Data starts row 5
    # Total controls = 93 -> rows 5 to 97
    control_rows = [row[0] for row in ws.iter_rows(min_row=5, max_col=1, values_only=True) if row[0]]
    assert len(control_rows) == 93, f"Esperado 93 controles en Excel, encontrado {len(control_rows)}"
    assert "A.5.1" in control_rows
    assert "A.8.34" in control_rows


def test_soa_export_csv_endpoint(client):
    # Act
    response = client.get("/soa/export/csv")

    # Assert HTTP headers
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

    # Decode content (handling UTF-8 BOM)
    content_text = response.content.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(content_text))
    rows = list(reader)

    # 1 header row + 93 data rows = 94 rows
    assert len(rows) == 94, f"Esperado 94 filas en CSV (1 cabecera + 93 controles), obtenido {len(rows)}"
    header = rows[0]
    assert "Identificador" in header
    assert "Es Aplicable" in header
    assert "Estado de Implementación" in header

    # Verify first and last control codes in rows
    first_ctrl_code = rows[1][0]
    last_ctrl_code = rows[-1][0]
    assert first_ctrl_code == "A.5.1"
    assert last_ctrl_code == "A.8.34"
