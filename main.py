import json
import os

from models.clients import clients , regular_clients, premium_clients, corporate_clients

def main():
    while True:
        menu = int(input(
            "SISTEMA DE GESTIÓN DE CLIENTES\n"
            "1- Gestión de clientes\n"
            "2- Beneficios\n"
            "3- Salir\n"
        ))
        if menu < 1 or menu > 3:
            print("elija una opcion correcta")
            continue
        if menu == 1 :
            while True:
                sub = input(
                    "\nGESTIÓN DE CLIENTES\n"
                    "1- Agregar cliente\n"
                    "2- Eliminar cliente\n"
                    "3- Editar cliente\n"
                    "4- Visualizar cliente\n"
                    "5- Volver\n"
                    "> "
                ).strip()

                match sub:
                    case "1":
                        print("\nAGREGAR CLIENTE")
                        client_type = input(
                            "¿Qué tipo de cliente desea agregar?\n"
                            "1- Cliente regular\n"
                            "2- Cliente premium\n"
                            "3- Cliente corporativo\n"
                            "> "
                        ).strip()

                        name = input("Ingrese el nombre del cliente: ").strip()
                        email = input("Ingrese el email del cliente: ").strip()
                        address_raw = input("Ingrese la direccion (ENTER = None): ").strip()
                        active_raw = input("Cliente activo? (y/n): ").strip().lower()

                        address = None if address_raw == "" else address_raw
                        active = True if active_raw in ("y", "yes", "s", "si", "sí") else False

                        if client_type == "1":
                            c = regular_clients(0, name, email, address, active)
                        elif client_type == "2":
                            c = premium_clients(0, name, email, address, active)
                        elif client_type == "3":
                            c = corporate_clients(0, name, email, address, active)
                        else:
                            print("Tipo inválido")
                            continue

                        clients.add_clients(lista=[c])
                        print("✓ Cliente agregado y guardado en bd/clients.json")
                    case "2":
                        print("\nELIMINAR CLIENTE")
                        cid = input("Ingrese el id a eliminar: ").strip()

                        result = clients.delete_clients(id=cid)

                        if result is False:
                            print("No existe un cliente con ese id.")
                        else:
                            print("✓ Cliente eliminado.")
                            print("Registro eliminado:", result)
                    case "3":
                        print("\nEDITAR CLIENTE")
                        cid = input("Ingrese el id a editar: ").strip()
                        print(
                            "\n¿Qué campo desea cambiar?\n"
                            "1- name\n"
                            "2- email\n"
                            "3- address\n"
                            "4- active\n"
                            "5- type (regular/premium/corporate)\n"
                        )
                        opt = input("> ").strip()
                        field_map = {
                            "1": "name",
                            "2": "email",
                            "3": "address",
                            "4": "active",
                            "5": "type",
                        }
                        if opt not in field_map:
                            print("Opción inválida")
                            continue
                        field = field_map[opt]
                        if field == "active":
                            value = input("Confirmar active (y/n): ").strip()
                        elif field == "type":
                            t = input(
                                "Nuevo type:\n"
                                "1- regular\n"
                                "2- premium\n"
                                "3- corporate\n"
                                "> ").strip()
                            type_map = {"1": "regular", "2": "premium", "3": "corporate"}
                            if t not in type_map:
                                print("Tipo inválido")
                                continue
                            value = type_map[t].strip()
                        elif field == "address":
                            value = input("Nueva address (ENTER para None): ")
                        else:
                            value = input(f"Nuevo {field}: ").strip()

                        try:
                            result = clients.modify_clients(id=cid, field=field, value=value)
                        except ValueError as e:
                            print("Error:", e)
                            continue

                        if result is False:
                            print("No existe un cliente con ese id.")
                        else:
                            print("Cliente actualizado:")
                            print(result)
                    case "4":
                        clients.view_clients()
                    case "5":
                        break
                    case _:
                        print("Elija una opción correcta")
        if menu == 2 :
            op = input(
            "BENEFICIOS\n"
            "1- Simulación de compra\n"
            "2- Salir\n"
            "> "
            ).strip()
            match op:
                case "1":
                    cid = input("Ingrese id del cliente: ").strip()
                    amount = input("Ingrese monto inicial: ").strip()

                    result = clients.discount_simulation(id=cid, amount=amount)

                    if result is False:
                        print("No existe un cliente con ese id.")
                case "2":
                    break
        elif menu == 3:
            break
main()