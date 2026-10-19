# controller/factory_escenarios.py
# ------------------------------------------------------------
# Fabrica de escenarios. Aplicamos el patron Factory Method.
# Devuelve un diccionario con los parametros del escenario
# segun la opcion elegida por el usuario.
# ------------------------------------------------------------


class FactoryEscenarios:

    def crear_escenario(self, opcion):
        if opcion == 1:
            return {"nombre": "Estable", "lambd": 2.0, "mu": 3.0}
        elif opcion == 2:
            return {"nombre": "Mayor utilizacion", "lambd": 2.5, "mu": 3.0}
        elif opcion == 3:
            return {"nombre": "Cerca de saturacion", "lambd": 2.9, "mu": 3.0}
        else:
            return None


# ------------------------------------------------------------
# Bloque de prueba rapida
# ------------------------------------------------------------
if __name__ == "__main__":
    fabrica = FactoryEscenarios()
    for i in range(1, 4):
        print(fabrica.crear_escenario(i))