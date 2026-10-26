package view;

import model.Resultado;

public class VistaConsola {
    public void mostrarInicio() {
        System.out.println("=================================================");
        System.out.println("   INICIANDO SIMULACIÓN MODELO EPIDEMIOLÓGICO SIR");
        System.out.println("=================================================");
    }

    public void mostrarPaso(Resultado resultado) {
        System.out.printf("Paso %3d: S = %3d | I = %3d | R = %3d%n",
                resultado.getTiempo(), resultado.getSusceptibles(),
                resultado.getInfectados(), resultado.getRecuperados());
    }

    public void mostrarFin(String rutaArchivo) {
        System.out.println("=================================================");
        System.out.println("Simulación finalizada.");
        System.out.println("Archivo CSV generado: " + rutaArchivo);
        System.out.println("=================================================");
    }

    public void mostrarError(String mensaje) {
        System.err.println("ERROR: " + mensaje);
    }
}
