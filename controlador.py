from views import GestorEstudiantes, GestorMaterias, GestorMatriculas


class Controlador:
    def __init__(self):
        self.estudiantes = GestorEstudiantes()
        self.materias = GestorMaterias()
        self.matriculas = GestorMatriculas(self.estudiantes, self.materias)

    def crear_estudiante(self, datos):
        return self.estudiantes.crear_estudiante(datos)

    def obtener_estudiantes(self):
        return self.estudiantes.obtener_estudiantes()

    def obtener_estudiante(self, id):
        return self.estudiantes.obtener_estudiante(id)

    def buscar_estudiantes(self, termino):
        return self.estudiantes.buscar_estudiantes(termino)

    def actualizar_estudiante(self, id, cambios):
        return self.estudiantes.actualizar_estudiante(id, cambios)

    def eliminar_estudiante(self, id):
        return self.estudiantes.eliminar_estudiante(id)

    def crear_materia(self, datos):
        return self.materias.crear_materia(datos)

    def obtener_materias(self):
        return self.materias.obtener_materias()

    def obtener_materia(self, id):
        return self.materias.obtener_materia(id)

    def buscar_materias(self, termino):
        return self.materias.buscar_materias(termino)

    def actualizar_materia(self, id, cambios):
        return self.materias.actualizar_materia(id, cambios)

    def eliminar_materia(self, id):
        return self.materias.eliminar_materia(id)

    def crear_matricula(self, datos):
        return self.matriculas.crear_matricula(datos)

    def obtener_matriculas(self):
        return self.matriculas.obtener_matriculas()

    def obtener_matricula(self, id):
        return self.matriculas.obtener_matricula(id)

    def registrar_nota(self, id, nota):
        return self.matriculas.registrar_nota(id, nota)

    def retirar_matricula(self, id):
        return self.matriculas.retirar_matricula(id)

    def certificado(self, id):
        return self.matriculas.certificado(id)

    def promedio_de_estudiante(self, id):
        return self.matriculas.promedio_de_estudiante(id)

    def resumen(self):
        estudiantes = self.estudiantes.obtener_estudiantes()
        carreras = sorted({e.carrera for e in estudiantes})
        aprobadas = [m for m in self.matriculas.obtener_matriculas() if m.esta_aprobada()]
        return {
            "estudiantes": len(estudiantes),
            "carreras": carreras,
            "sin_cupo": self.materias.materias_sin_cupo(),
            "aprobadas": len(aprobadas),
        }
