def test_crud_producto(client):
    r = client.post("/api/productos", json={"nombre": "Teclado", "precio": "150.50", "stock": 5})
    assert r.status_code == 201 and r.json["precio"] == 150.5
    pid = r.json["id"]
    r = client.put(f"/api/productos/{pid}", json={"nombre": "Teclado", "precio": 99, "stock": 3, "activo": False})
    assert r.status_code == 200 and r.json["activo"] is False
    assert client.delete(f"/api/productos/{pid}").status_code == 204


def test_producto_invalido(client):
    assert client.post("/api/productos", json={"nombre": "X", "precio": -1, "stock": 1}).status_code == 400
    assert client.post("/api/productos", json={"nombre": "X"}).status_code == 400


def test_pedido_descuenta_y_restaura_stock(client):
    c = client.post("/api/clientes", json={"nombre": "A", "correo": "a@example.com"}).json
    p = client.post("/api/productos", json={"nombre": "P", "precio": 10, "stock": 5}).json
    r = client.post("/api/pedidos", json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 3})
    assert r.status_code == 201 and r.json["total"] == 30
    assert client.get(f"/api/productos/{p['id']}").json["stock"] == 2
    assert client.post("/api/pedidos", json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 9}).status_code == 409
    oid = r.json["id"]
    assert client.delete(f"/api/pedidos/{oid}").status_code == 409
    client.put(f"/api/pedidos/{oid}", json={"estado": "cancelado"})
    assert client.get(f"/api/productos/{p['id']}").json["stock"] == 5
    assert client.delete(f"/api/pedidos/{oid}").status_code == 204
