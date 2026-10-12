import json
import os
from datetime import date
from models import Estudiante, Materia, Matricula


def es_email_valido(email):
    return "@" in email and "." in email.split("@")[-1]


class GestorBase:
    def __init__(self, ruta, clase):
        self.ruta = ruta
        self.clase = clase
        self.objetos = []
        self.cargar()

    def cargar(self):
        if not os.path.exists(self.ruta):
            return
        with open(self.ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for d in datos:
            self.objetos.append(self.clase.desde_diccionario(d))

    def guardar(self):
        os.makedirs("data", exist_ok=True)
        datos = [o.a_diccionario() for o in self.objetos]
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def siguiente_id(self):
        if len(self.objetos) == 0:
            return 1
        return max(o.id for o in self.objetos) + 1

    def obtener_por_id(self, id):
        for o in self.objetos:
            if o.id == id:
                return o
        return None

    def ids_registrados(self):
        return {o.id for o in self.objetos}


class GestorEstudiantes(GestorBase):
    def __init__(self, ruta="data/estudiantes.json"):
        super().__init__(ruta, Estudiante)

    def carnets_registrados(self, excepto_id=None):
        # CONJUNTO de carnets usados: preguntar 'x in conjunto' es instantáneo y no admite repetidos.
        return {e.carnet.upper() for e in self.objetos if e.id != excepto_id}

    def emails_registrados(self, excepto_id=None):
        return {e.email.lower() for e in self.objetos if e.id != excepto_id}

    def validar_estudiante(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ["nombre", "apellido", "email", "carnet"]:
                if not datos.get(campo):
                    return f"El campo {campo} es obligatorio"
        if "email" in datos:
            if not es_email_valido(datos["email"]):
                return "El email no es válido"
            if datos["email"].lower() in self.emails_registrados(id_actual):
                return "El email ya existe"
        if "carnet" in datos:
            if datos["carnet"].upper() in self.carnets_registrados(id_actual):
                return "El carnet ya existe"
        return None

    def crear_estudiante(self, datos):
        # TUPLA (exito, mensaje): lleva dos datos juntos y nadie los puede modificar después.
        mensaje = self.validar_estudiante(datos)
        if mensaje:
            return False, mensaje
        estudiante = Estudiante(
            self.siguiente_id(),
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"].upper(),
            datos.get("carrera", ""),
        )
        self.objetos.append(estudiante)
        self.guardar()
        return True, "Estudiante creado"

    def obtener_estudiantes(self):
        return self.objetos

    def obtener_estudiante(self, id):
        return self.obtener_por_id(id)

    def buscar_estudiantes(self, termino):
        termino = termino.lower()
        resultado = []
        for e in self.objetos:
            if termino in e.nombre.lower() or termino in e.apellido.lower() or termino in e.carnet.lower():
                resultado.append(e)
        return resultado

    def actualizar_estudiante(self, id, cambios):
        estudiante = self.obtener_por_id(id)
        if estudiante is None:
            return False, "Estudiante no encontrado"
        mensaje = self.validar_estudiante(cambios, id)
        if mensaje:
            return False, mensaje
        for campo, valor in cambios.items():
            setattr(estudiante, campo, valor)
        estudiante.carnet = estudiante.carnet.upper()
        self.guardar()
        return True, "Estudiante actualizado"

    def eliminar_estudiante(self, id):
        estudiante = self.obtener_por_id(id)
        if estudiante is None:
            return False, "Estudiante no encontrado"
        self.objetos.remove(estudiante)
        self.guardar()
        return True, "Estudiante eliminado"


class GestorMaterias(GestorBase):
    def __init__(self, ruta="data/materias.json"):
        super().__init__(ruta, Materia)

    def codigos_registrados(self, excepto_id=None):
        return {m.codigo.upper() for m in self.objetos if m.id != excepto_id}

    def validar_materia(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ["nombre", "codigo", "creditos", "cupos"]:
                if campo not in datos or datos[campo] == "":
                    return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            if datos["codigo"].upper() in self.codigos_registrados(id_actual):
                return "El código ya existe"
        if "creditos" in datos:
            try:
                creditos = int(datos["creditos"])
            except ValueError:
                return "Los créditos deben ser un número entero"
            if creditos < 1 or creditos > 10:
                return "Los créditos deben estar entre 1 y 10"
        if "cupos" in datos:
            try:
                cupos = int(datos["cupos"])
            except ValueError:
                return "Los cupos deben ser un número entero"
            if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:
                return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
        return None

    def crear_materia(self, datos):
        mensaje = self.validar_materia(datos)
        if mensaje:
            return False, mensaje
        materia = Materia(
            self.siguiente_id(),
            datos["nombre"],
            datos["codigo"].upper(),
            datos["creditos"],
            datos["cupos"],
        )
        self.objetos.append(materia)
        self.guardar()
        return True, "Materia creada"

    def obtener_materias(self):
        return self.objetos

    def obtener_materia(self, id):
        return self.obtener_por_id(id)

    def buscar_materias(self, termino):
        termino = termino.lower()
        resultado = []
        for m in self.objetos:
            if termino in m.nombre.lower() or termino in m.codigo.lower():
                resultado.append(m)
        return resultado

    def actualizar_materia(self, id, cambios):
        materia = self.obtener_por_id(id)
        if materia is None:
            return False, "Materia no encontrada"
        mensaje = self.validar_materia(cambios, id)
        if mensaje:
            return False, mensaje
        for campo, valor in cambios.items():
            setattr(materia, campo, valor)
        materia.creditos = int(materia.creditos)
        materia.cupos = int(materia.cupos)
        materia.codigo = materia.codigo.upper()
        self.guardar()
        return True, "Materia actualizada"

    def eliminar_materia(self, id):
        materia = self.obtener_por_id(id)
        if materia is None:
            return False, "Materia no encontrada"
        self.objetos.remove(materia)
        self.guardar()
        return True, "Materia eliminada"

    def materias_sin_cupo(self):
        return [m for m in self.objetos if not m.hay_cupo()]


class GestorMatriculas(GestorBase):
    def __init__(self, gestor_estudiantes, gestor_materias, ruta="data/matriculas.json"):
        self.estudiantes = gestor_estudiantes
        self.materias = gestor_materias
        super().__init__(ruta, Matricula)

    def validar_matricula(self, datos):
        if datos["estudiante_id"] not in self.estudiantes.ids_registrados():
            return "El estudiante no existe"
        if datos["materia_id"] not in self.materias.ids_registrados():
            return "La materia no existe"
        materia = self.materias.obtener_por_id(datos["materia_id"])
        if not materia.hay_cupo():
            return "No quedan cupos"
        for m in self.objetos:
            if (m.estudiante_id == datos["estudiante_id"]
                    and m.materia_id == datos["materia_id"]
                    and m.periodo == datos["periodo"]):
                return "Ya está matriculado en esa materia en ese periodo"
        if "nota" in datos and not Materia.es_nota_valida(datos["nota"]):
            return "La nota debe estar entre 0 y 20"
        return None

    def crear_matricula(self, datos):
        mensaje = self.validar_matricula(datos)
        if mensaje:
            return False, mensaje
        materia = self.materias.obtener_por_id(datos["materia_id"])
        matricula = Matricula(
            self.siguiente_id(),
            datos["estudiante_id"],
            datos["materia_id"],
            datos["periodo"],
            datos.get("nota", 0),
            str(date.today()),
        )
        self.objetos.append(matricula)
        self.guardar()
        materia.ocupar_cupo()
        self.materias.guardar()
        return True, "Matrícula creada"

    def obtener_matriculas(self):
        return self.objetos

    def obtener_matricula(self, id):
        return self.obtener_por_id(id)

    def registrar_nota(self, id, nota):
        matricula = self.obtener_por_id(id)
        if matricula is None:
            return False, "Matrícula no encontrada"
        if not Materia.es_nota_valida(nota):
            return False, "La nota debe estar entre 0 y 20"
        matricula.nota = float(nota)
        self.guardar()
        return True, "Nota registrada"

    def retirar_matricula(self, id):
        matricula = self.obtener_por_id(id)
        if matricula is None:
            return False, "Matrícula no encontrada"
        materia = self.materias.obtener_por_id(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()
        self.objetos.remove(matricula)
        self.guardar()
        return True, "Matrícula retirada"

    def certificado(self, id):
        matricula = self.obtener_por_id(id)
        if matricula is None:
            return None
        # DICCIONARIO ÍNDICE {id: objeto}: encuentro al estudiante y la materia directo por su id.
        indice_estudiantes = {e.id: e for e in self.estudiantes.obtener_estudiantes()}
        indice_materias = {m.id: m for m in self.materias.obtener_materias()}
        estudiante = indice_estudiantes[matricula.estudiante_id]
        materia = indice_materias[matricula.materia_id]
        lineas = [
            f"CERTIFICADO #{matricula.id}   periodo: {matricula.periodo}",
            f"Estudiante: {estudiante.nombre} {estudiante.apellido}   ({estudiante.carnet})",
            f"Materia   : {materia.nombre}   ({materia.codigo}) - {materia.creditos} créditos",
            "─" * 40,
            f"Nota      : {matricula.nota}",
            f"Estado    : {matricula.estado()}",
        ]
        return "\n".join(lineas)

    def matriculas_por_estudiante(self):
        # DICCIONARIO DE LISTAS: un estudiante tiene varias matrículas y setdefault crea su lista.
        grupos = {}
        for m in self.objetos:
            grupos.setdefault(m.estudiante_id, []).append(m)
        return grupos

    def promedio_de_estudiante(self, id):
        lista = self.matriculas_por_estudiante().get(id, [])
        if len(lista) == 0:
            return 0
        return sum(m.nota for m in lista) / len(lista)
