# CRUD de Ventas con Vue y Flask

Este proyecto es una aplicación CRUD para administrar clientes, productos y pedidos.

La aplicación está dividida en dos partes: el frontend, realizado con Vue 3, y el backend, realizado con Flask. Para comunicar ambas partes se utiliza Axios y para guardar la información se utiliza una base de datos SQLite con Flask-SQLAlchemy.

## Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.11 o superior
- Node.js
- Git

## Backend

El backend contiene la API, la conexión con la base de datos, los modelos y las validaciones.

Para ejecutarlo desde PowerShell:

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
copy .env.example .env
flask --app run.py db upgrade
flask --app run.py run --debug
```

El backend se ejecuta en:

`http://127.0.0.1:5000`

Para comprobar que está funcionando se puede utilizar:

`http://127.0.0.1:5000/health`

## Frontend

El frontend contiene las páginas que utiliza el usuario para trabajar con los datos.

Para ejecutarlo se debe abrir otra terminal y utilizar:

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Después se puede abrir la aplicación desde:

`http://localhost:5173`

## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

```text
crud-vue-flask/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── clientes.py
│   │   │   ├── productos.py
│   │   │   └── pedidos.py
│   │   ├── __init__.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── errors.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    └── src/
        ├── api/
        ├── components/
        ├── views/
        ├── router/
        ├── App.vue
        └── main.js
```

En `backend` se encuentra todo lo relacionado con Flask y la base de datos. En `models.py` están definidas las tablas de clientes, productos y pedidos, mientras que en la carpeta `api` están las operaciones para crear, consultar, actualizar y eliminar los registros.

En `frontend` se encuentra la parte visual realizada con Vue 3. Las vistas corresponden a las páginas de clientes, productos, pedidos y el inicio. También se utilizan componentes reutilizables y Vue Router para navegar entre las diferentes páginas.

Axios permite que el frontend se comunique con la API de Flask para enviar y recibir la información.

## Base de datos

La aplicación utiliza SQLite y contiene tres tablas principales:

- `clientes`: guarda los datos de los clientes.
- `productos`: guarda la información de los productos, su precio y stock.
- `pedidos`: guarda los pedidos y los relaciona con un cliente y un producto.

Los pedidos utilizan `cliente_id` y `producto_id` para relacionarse con las otras tablas.

## Validaciones

La aplicación cuenta con validaciones tanto en el frontend como en el backend.

En clientes se valida principalmente el nombre y el correo electrónico. En productos se validan datos como el nombre, precio y stock. En pedidos se verifica que exista el cliente y el producto, que la cantidad sea válida y que exista suficiente stock.

También se evita eliminar clientes o productos que tengan pedidos relacionados.

## Funcionamiento de los pedidos

Cuando se crea un pedido, la cantidad solicitada se descuenta del stock del producto.

Los pedidos pueden tener los estados:

- Pendiente
- Pagado
- Enviado
- Cancelado

Cuando un pedido se cancela, la cantidad se devuelve al stock. Para eliminar un pedido primero debe estar cancelado.

## Pruebas

El proyecto incluye pruebas para clientes y productos.

Para ejecutarlas desde la carpeta `backend` se utiliza:

```powershell
pytest
```