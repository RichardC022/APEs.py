package controller;

import model.ModeloSIR;
import model.Resultado;
import view.VistaConsola;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class ControladorSimulacion {
    private final ModeloSIR modelo;
    private final VistaConsola vista;
    private final int pasosTotales;
    private final List<Resultado> historialResultados;
    private final Path rutaSalida;

    public ControladorSimulacion(int poblacion, int infectadosIniciales,
            double beta, double gamma, int pasosTotales, long semilla) {
        if (pasosTotales < 0) {
            throw new IllegalArgumentException("El número de pasos no puede ser negativo.");
        }
        this.modelo = new ModeloSIR(poblacion, infectadosIniciales, beta, gamma, semilla);
        this.vista = new VistaConsola();
        this.pasosTotales = pasosTotales;
        this.historialResultados = new ArrayList<>();
        this.rutaSalida = Path.of("resultados_java.csv").toAbsolutePath();
    }

    public boolean ejecutar() {
        vista.mostrarInicio();

        Resultado estadoInicial = modelo.obtenerResultadoActual();
        historialResultados.add(estadoInicial);
        vista.mostrarPaso(estadoInicial);

        for (int paso = 1; paso <= pasosTotales; paso++) {
            modelo.avanzarPaso();
            Resultado resultado = modelo.obtenerResultadoActual();
            historialResultados.add(resultado);
            vista.mostrarPaso(resultado);
        }

        if (!guardarCSV()) {
            return false;
        }

        vista.mostrarFin(rutaSalida.toString());
        return true;
    }

    private boolean guardarCSV() {
        for (Resultado resultado : historialResultados) {
            int total = resultado.getSusceptibles()
                    + resultado.getInfectados()
                    + resultado.getRecuperados();
            if (total != modelo.getPoblacionTotal()) {
                vista.mostrarError("La población no se conserva en t="
                        + resultado.getTiempo() + ": " + total);
                return false;
            }
        }

        try (BufferedWriter writer = Files.newBufferedWriter(
                rutaSalida, StandardCharsets.UTF_8)) {
            writer.write("tiempo,susceptibles,infectados,recuperados");
            writer.newLine();
            for (Resultado resultado : historialResultados) {
                writer.write(resultado.toCSV());
                writer.newLine();
            }
            return true;
        } catch (IOException e) {
            vista.mostrarError("No se pudo escribir " + rutaSalida
                    + ": " + e.getMessage());
            return false;
        }
    }
}
