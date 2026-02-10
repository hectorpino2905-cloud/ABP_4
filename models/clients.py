from dataclasses import dataclass
from typing import Optional
import json
import os

@dataclass
class clients:
    id: int
    name: str
    email: str
    address: Optional[str] = None
    active: bool = True

    def discount(self) -> float:
        return 0.0
    def apply_discount(self, amount: int) -> float:
        return amount * (1 - self.discount())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "active": self.active,
            "type": self.get_type()
        }
    def get_type(self) -> str:
        return "regular"

    @staticmethod
    def add_clients(**kwargs):
        route = kwargs.get("ruta") or "bd/clients.json"
        clients_list = kwargs.get("lista")
        if not clients_list:
            raise ValueError("faltan datos: lista vacía o no enviada (use lista=[...])")
        os.makedirs(os.path.dirname(route), exist_ok=True)
        try:
            with open(route, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        if not isinstance(data, list):
            raise ValueError("clients.json debe ser una LISTA (ej: [])")
        ids = []
        for item in data:
            if isinstance(item, dict):
                try:
                    ids.append(int(item.get("id", 0)))
                except (TypeError, ValueError):
                    pass
        next_id = 1 if not ids else max(ids) + 1
        for client in clients_list:
            client.id = next_id
            data.append(client.to_dict())
            next_id += 1
        with open(route, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return route
    @staticmethod
    def modify_clients(**kwargs):
        import json
        import os

        route = kwargs.get("ruta") or "bd/clients.json"
        client_id = kwargs.get("id")
        field = kwargs.get("field")
        value = kwargs.get("value")

        if client_id is None or field is None:
            raise ValueError("faltan datos: id y field")
        try:
            client_id = int(str(client_id).strip())
        except ValueError:
            raise ValueError("id inválido")

        field = str(field).strip().lower()
        try:
            with open(route, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        if not isinstance(data, list):
            raise ValueError("clients.json debe ser una LISTA (ej: [])")
        target = None
        for item in data:
            if isinstance(item, dict) and int(item.get("id", -1)) == client_id:
                target = item
                break
        if target is None:
            return False  
        if field == "id":
            raise ValueError("No se puede modificar el id")
        if field == "name":
            target["name"] = str(value).strip()
        elif field == "email":
            target["email"] = str(value).strip()
        elif field == "address":
            if value is None:
                target["address"] = None
            else:
                v = str(value).strip()
                target["address"] = None if v == "" or v == "-" else v
        elif field == "active":
            if isinstance(value, bool):
                target["active"] = value
            else:
                v = str(value).strip().lower()
                target["active"] = True if v in ("y", "yes", "s", "si", "sí", "true", "1") else False
        elif field == "type":
            v = str(value).strip().lower()
            if v not in ("regular", "premium", "corporate"):
                raise ValueError("type inválido (use regular/premium/corporate)")
            target["type"] = v
        else:
            raise ValueError("Campo inválido")
        os.makedirs(os.path.dirname(route), exist_ok=True)
        with open(route, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return target 
    def delete_clients(**kwargs):
        route = kwargs.get("ruta") or "bd/clients.json"
        client_id = kwargs.get("id")

        if client_id is None:
            raise ValueError("Faltan datos")
        try:
            client_id = int(str(client_id).strip())
        except ValueError:
            raise ValueError("id inválido")
        try:
            with open(route, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        if not isinstance(data, list):
            raise ValueError("clients.json debe ser una LISTA (ej: [])")
        deleted_id = None
        new_data = []

        for item in data:
            if isinstance(item, dict) and int(item.get("id", -1)) == client_id:
                deleted_id = item
            else:
                new_data.append(item)
        if deleted_id is None:
            return False

        os.makedirs(os.path.dirname(route), exist_ok=True)

        with open(route, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        return deleted_id
    @staticmethod
    def view_clients(**kwargs):
        import json
        route = kwargs.get("ruta") or "bd/clients.json"
        try:
            with open(route, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        if not isinstance(data, list):
            raise ValueError("clients.json debe ser una LISTA (ej: [])")
        if not data:
            print("(No clients)")
            return []
        data_sorted = sorted(
            [x for x in data if isinstance(x, dict)],
            key=lambda item: int(item.get("id", 0))
        )
        print("\n=== CLIENTS LIST ===")
        for item in data_sorted:
            print("-" * 40)
            print(
                f"ID: {item.get('id')} | "
                f"Type: {item.get('type')} | "
                f"Name: {item.get('name')} | "
                f"Email: {item.get('email')} | "
                f"Active: {item.get('active')}"
            )
        print("-" * 40)
        return data_sorted
    @staticmethod
    def discount_simulation(**kwargs):
        import json
        route = kwargs.get("ruta") or "bd/clients.json"
        client_id = kwargs.get("id")
        amount = kwargs.get("amount")
        if client_id is None or amount is None:
            raise ValueError("faltan datos:")
        try:
            client_id = int(str(client_id).strip())
        except ValueError:
            raise ValueError("id inválido")
        try:
            amount = float(str(amount).replace(",", ".").strip())
        except ValueError:
            raise ValueError("monto inválido")
        try:
            with open(route, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        if not isinstance(data, list):
            raise ValueError("clients.json debe ser una LISTA (ej: [])")
        record = None
        for item in data:
            if isinstance(item, dict) and int(item.get("id", -1)) == client_id:
                record = item
                break
        if record is None:
            return False  
        ctype = str(record.get("type", "regular")).lower()
        if ctype not in ("regular", "premium", "corporate"):
            ctype = "regular" 
        if ctype == "premium":
            obj = premium_clients(0, "tmp", "tmp@x.com", None, True)
        elif ctype == "corporate":
            obj = corporate_clients(0, "tmp", "tmp@x.com", None, True)
        else:
            obj = regular_clients(0, "tmp", "tmp@x.com", None, True)

        rate = obj.discount()  # 0.0 / 0.05 / 0.1
        discount_amount = amount * rate
        final_price = amount - discount_amount

        # imprimir ordenado
        print("\n=== DISCOUNT SIMULATION ===")
        print(f"Client ID: {record.get('id')} | Type: {ctype}")
        print("-" * 30)
        print(f"Initial amount: {amount}")
        print(f"Discount rate: {rate}")
        print(f"Discount amount: {discount_amount}")
        print(f"Final price: {final_price}")
        print("-" * 30)
        return {
            "id": record.get("id"),
            "type": ctype,
            "initial": amount,
            "rate": rate,
            "discount_amount": discount_amount,
            "final": final_price,
        }
@dataclass
class regular_clients(clients):
    def discount(self) -> float:
        return 0.0
    

@dataclass
class premium_clients(clients):
    def discount(self) -> float:
        return 0.05
    def get_type(self) -> str:
        return "premium"
@dataclass
class corporate_clients(clients):
    def discount(self) -> float:
        return 0.1
    def get_type(self) -> str:
        return "corporate"