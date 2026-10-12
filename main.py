from controlador import Controlador

controlador = Controlador()


def mostrar_lista(lista):
    if len(lista) == 0:
        print("No hay registros")
    for o in lista:
        print(o.id, "-", o.etiqueta())


def mostrar_detalle(objeto):
    if objeto is None:
        print("No existe")
        return
    print(objeto.etiqueta())
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {clave}: {valor}")


def pedir_id():
    try:
        return int(input("ID: "))
    except ValueError:
        return None


def pedir_cambios(campos):
    cambios = {}
    for campo in campos:
        valor = input(f"Nuevo {campo} (Enter para dejar igual): ")
        if valor != "":
            cambios[campo] = valor
    return cambios


def opcion_crear_estudiante():
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
    }
    ok, mensaje = controlador.crear_estudiante(datos)
    print(mensaje)


def opcion_listar_estudiantes():
    mostrar_lista(controlador.obtener_estudiantes())


def opcion_buscar_estudiantes():
    texto = input("Buscar: ")
    mostrar_lista(controlador.buscar_estudiantes(texto))


def opcion_ver_estudiante():
    mostrar_detalle(controlador.obtener_estudiante(pedir_id()))


def opcion_actualizar_estudiante():
    id = pedir_id()
    cambios = pedir_cambios(["nombre", "apellido", "email", "carnet", "carrera"])
    ok, mensaje = controlador.actualizar_estudiante(id, cambios)
    print(mensaje)


def opcion_eliminar_estudiante():
    ok, mensaje = controlador.eliminar_estudiante(pedir_id())
    print(mensaje)


def menu_estudiantes():
    while True:
        print("\n--- Estudiantes ---")
        print("1. Crear estudiante")
        print("2. Ver todos")
        print("3. Buscar")
        print("4. Ver por id")
        print("5. Actualizar")
        print("6. Eliminar")
        print("0. Volver")
        opcion = input("Elige: ")
        if opcion == "1":
            opcion_crear_estudiante()
        elif opcion == "2":
            opcion_listar_estudiantes()
        elif opcion == "3":
            opcion_buscar_estudiantes()
        elif opcion == "4":
            opcion_ver_estudiante()
        elif opcion == "5":
            opcion_actualizar_estudiante()
        elif opcion == "6":
            opcion_eliminar_estudiante()
        elif opcion == "0":
            break
        else:
            print("Opción no válida")


def opcion_crear_materia():
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código: "),
        "creditos": input("Créditos (1-10): "),
        "cupos": input("Cupos (0-30): "),
    }
    ok, mensaje = controlador.crear_materia(datos)
    print(mensaje)


def opcion_listar_materias():
    mostrar_lista(controlador.obtener_materias())


def opcion_buscar_materias():
    texto = input("Buscar: ")
    mostrar_lista(controlador.buscar_materias(texto))


def opcion_ver_materia():
    mostrar_detalle(controlador.obtener_materia(pedir_id()))


def opcion_actualizar_materia():
    id = pedir_id()
    cambios = pedir_cambios(["nombre", "codigo", "creditos", "cupos"])
    ok, mensaje = controlador.actualizar_materia(id, cambios)
    print(mensaje)


def opcion_eliminar_materia():
    ok, mensaje = controlador.eliminar_materia(pedir_id())
    print(mensaje)


def menu_materias():
    while True:
        print("\n--- Materias ---")
        print("1. Crear materia")
        print("2. Ver todas")
        print("3. Buscar")
        print("4. Ver por id")
        print("5. Actualizar")
        print("6. Eliminar")
        print("0. Volver")
        opcion = input("Elige: ")
        if opcion == "1":
            opcion_crear_materia()
        elif opcion == "2":
            opcion_listar_materias()
        elif opcion == "3":
            opcion_buscar_materias()
        elif opcion == "4":
            opcion_ver_materia()
        elif opcion == "5":
            opcion_actualizar_materia()
        elif opcion == "6":
            opcion_eliminar_materia()
        elif opcion == "0":
            break
        else:
            print("Opción no válida")


def opcion_matricular():
    try:
        datos = {
            "estudiante_id": int(input("ID del estudiante: ")),
            "materia_id": int(input("ID de la materia: ")),
            "periodo": input("Periodo (ej. 2026-1): "),
        }
    except ValueError:
        print("Los ids deben ser números")
        return
    ok, mensaje = controlador.crear_matricula(datos)
    print(mensaje)


def opcion_listar_matriculas():
    mostrar_lista(controlador.obtener_matriculas())


def opcion_registrar_nota():
    id = pedir_id()
    nota = input("Nota (0-20): ")
    ok, mensaje = controlador.registrar_nota(id, nota)
    print(mensaje)


def opcion_certificado():
    texto = controlador.certificado(pedir_id())
    if texto is None:
        print("Matrícula no encontrada")
    else:
        print(texto)


def opcion_retirar_matricula():
    ok, mensaje = controlador.retirar_matricula(pedir_id())
    print(mensaje)


def menu_matriculas():
    while True:
        print("\n--- Matrículas ---")
        print("1. Matricular")
        print("2. Ver todas")
        print("3. Registrar nota")
        print("4. Ver certificado")
        print("5. Retirar matrícula")
        print("0. Volver")
        opcion = input("Elige: ")
        if opcion == "1":
            opcion_matricular()
        elif opcion == "2":
            opcion_listar_matriculas()
        elif opcion == "3":
            opcion_registrar_nota()
        elif opcion == "4":
            opcion_certificado()
        elif opcion == "5":
            opcion_retirar_matricula()
        elif opcion == "0":
            break
        else:
            print("Opción no válida")


def opcion_resumen():
    datos = controlador.resumen()
    print("Estudiantes:", datos["estudiantes"])
    print("Carreras distintas:", len(datos["carreras"]), datos["carreras"])
    print("Materias sin cupo:", len(datos["sin_cupo"]))
    print("Matrículas aprobadas:", datos["aprobadas"])


def menu():
    while True:
        print("\n--- Sistema Académico ---")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Matrículas")
        print("4. Resumen")
        print("0. Salir")
        opcion = input("Elige: ")
        if opcion == "1":
            menu_estudiantes()
        elif opcion == "2":
            menu_materias()
        elif opcion == "3":
            menu_matriculas()
        elif opcion == "4":
            opcion_resumen()
        elif opcion == "0":
            break
        else:
            print("Opción no válida")


menu()
