# ABP_4: Sistema Gestión Clientes y Beneficios

## Descripción
Proyecto en Python orientado a objetos para gestionar clientes (crear, visualizar, editar y eliminar) y simular beneficios mediante descuentos según el tipo de cliente (regular, premium, corporate).  
La persistencia de datos se realiza en un archivo JSON (`bd/clients.json`).

---

## Cómo ejecutar el proyecto
1. Abre una terminal en la carpeta raíz del proyecto (donde está `main.py`).
2. Ejecuta:

```bash
python main.py
```
---

## Estructura del proyecto

ABP_4/
├─ main.py
├─ readme.md
├─ bd/
│ └─ clients.json
├─ models/
│ ├─ init.py
│ └─ clients.py
└─ docs/
├─ diagrama.puml
└─ poo_importancia.md


---

## Requisitos
- Python 3.10+ (recomendado por `match/case`)
- No requiere librerías externas (solo estándar)

---

## Tipos de cliente y descuentos
- **regular** → 0%
- **premium** → 5%
- **corporate** → 10%

Estos descuentos se implementan con **polimorfismo** en las subclases:
- `regular_clients`
- `premium_clients`
- `corporate_clients`

---

## Base de datos (JSON)
Ruta por defecto:
- `bd/clients.json`

Formato actual:
- **Lista de diccionarios** (array JSON)

Ejemplo:
```json
[
  {
    "id": 1,
    "name": "juan",
    "email": "juan@juan.com",
    "address": null,
    "active": true,
    "type": "premium"
  }
]
```

## Métodos del sistema (resumen)

Los métodos principales están en `models/clients.py` y permiten gestionar el archivo `bd/clients.json` (formato: **lista de diccionarios**), además de simular descuentos según el tipo de cliente.

### `add_clients(lista=[...], ruta="bd/clients.json")`
Agrega uno o más clientes al JSON. Calcula el **id autoincremental** leyendo los ids existentes y asigna `max(id)+1` (o `1` si está vacío). Luego guarda cada objeto usando `to_dict()`.

### `view_clients(ruta="bd/clients.json")`
Lee el JSON y muestra en consola un listado de clientes ordenado por `id`. Devuelve la lista de registros (diccionarios) ordenada.

### `modify_clients(id=..., field=..., value=..., ruta="bd/clients.json")`
Edita un cliente buscándolo por `id`. Permite cambiar `name`, `email`, `address`, `active` y `type`. No permite modificar `id`. Guarda los cambios en el JSON y retorna el registro actualizado (o `False` si el id no existe).

### `delete_clients(id=..., ruta="bd/clients.json")`
Elimina un cliente por `id`, reescribiendo el JSON sin ese registro. Retorna el registro eliminado (o `False` si el id no existe).

### `discount_simulation(id=..., amount=..., ruta="bd/clients.json")`
Simula una compra: busca el cliente por `id`, obtiene su `type` desde el JSON y aplica el porcentaje retornado por `discount()` (polimorfismo según `regular/premium/corporate`). Imprime monto inicial, monto descontado y precio final. Retorna un diccionario con el resultado (o `False` si el id no existe).

---

## Métodos de instancia (POO)

### `discount()`
Retorna el porcentaje de descuento según el tipo de cliente. Se sobrescribe en las subclases (`regular_clients`, `premium_clients`, `corporate_clients`) para demostrar **polimorfismo**.

### `apply_discount(amount)`
Calcula el precio final aplicando el descuento del cliente: `amount * (1 - discount())`.

### `to_dict()`
Convierte el objeto cliente en un diccionario listo para guardar en JSON. Incluye `"type"` usando `get_type()`.

### `get_type()`
Devuelve el tipo del cliente (`regular`, `premium`, `corporate`). En `premium_clients` y `corporate_clients` se sobrescribe para guardar el tipo correcto.
