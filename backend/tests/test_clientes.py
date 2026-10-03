def test_crear_y_listar_cliente(client):
    r = client.post("/api/clientes", json={"nombre": "Cliente de prueba", "correo": "prueba@example.com"})
    assert r.status_code == 201
    assert r.json["nombre"] == "Cliente de prueba"
    r = client.get("/api/clientes")
    assert r.status_code == 200 and len(r.json) == 1


def test_correo_invalido_y_duplicado(client):
    assert client.post("/api/clientes", json={"nombre": "A", "correo": "malo"}).status_code == 400
    ok = {"nombre": "A", "correo": "a@example.com"}
    assert client.post("/api/clientes", json=ok).status_code == 201
    assert client.post("/api/clientes", json=ok).status_code == 409
