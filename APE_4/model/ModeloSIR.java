package model;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ModeloSIR {
    private final List<Individuo> poblacion;
    private final double beta;
    private final double gamma;
    private final Random random;
    private int tiempoActual;

    public ModeloSIR(int poblacionTotal, int infectadosIniciales, double beta,
            double gamma, long semilla) {
        validarParametros(poblacionTotal, infectadosIniciales, beta, gamma);

        this.beta = beta;
        this.gamma = gamma;
        this.random = new Random(semilla);
        this.poblacion = new ArrayList<>(poblacionTotal);
        this.tiempoActual = 0;

        for (int i = 0; i < poblacionTotal; i++) {
            Estado estadoInicial = i < infectadosIniciales
                    ? Estado.INFECTADO
                    : Estado.SUSCEPTIBLE;
            poblacion.add(new Individuo(i, estadoInicial));
        }
    }

    public void avanzarPaso() {
        List<Integer> indicesSusceptibles = new ArrayList<>();
        List<Integer> indicesInfectados = new ArrayList<>();

        for (int i = 0; i < poblacion.size(); i++) {
            Estado estado = poblacion.get(i).getEstado();
            if (estado == Estado.SUSCEPTIBLE) {
                indicesSusceptibles.add(i);
            } else if (estado == Estado.INFECTADO) {
                indicesInfectados.add(i);
            }
        }

        boolean[] nuevosContagios = new boolean[poblacion.size()];
        for (int indiceSusceptible : indicesSusceptibles) {
            for (int indiceInfectado : indicesInfectados) {
                if (random.nextDouble() < beta) {
                    nuevosContagios[indiceSusceptible] = true;
                    break;
                }
            }
        }

        boolean[] recuperaciones = new boolean[poblacion.size()];
        for (int indiceInfectado : indicesInfectados) {
            if (random.nextDouble() < gamma) {
                recuperaciones[indiceInfectado] = true;
            }
        }

        for (int i = 0; i < poblacion.size(); i++) {
            if (nuevosContagios[i]) {
                poblacion.get(i).infectar();
            } else if (recuperaciones[i]) {
                poblacion.get(i).recuperar();
            }
        }

        tiempoActual++;
    }

    public Resultado obtenerResultadoActual() {
        int susceptibles = 0;
        int infectados = 0;
        int recuperados = 0;

        for (Individuo individuo : poblacion) {
            switch (individuo.getEstado()) {
                case SUSCEPTIBLE:
                    susceptibles++;
                    break;
                case INFECTADO:
                    infectados++;
                    break;
                case RECUPERADO:
                    recuperados++;
                    break;
                default:
                    throw new IllegalStateException("Estado epidemiológico desconocido.");
            }
        }

        return new Resultado(tiempoActual, susceptibles, infectados, recuperados);
    }

    public int getPoblacionTotal() {
        return poblacion.size();
    }

    private static void validarParametros(int poblacionTotal, int infectadosIniciales,
            double beta, double gamma) {
        if (poblacionTotal <= 0) {
            throw new IllegalArgumentException("La población total debe ser positiva.");
        }
        if (infectadosIniciales < 0 || infectadosIniciales > poblacionTotal) {
            throw new IllegalArgumentException(
                    "La cantidad de infectados iniciales debe estar entre 0 y la población total.");
        }
        if (!Double.isFinite(beta) || beta < 0.0 || beta > 1.0) {
            throw new IllegalArgumentException("Beta debe ser una probabilidad entre 0 y 1.");
        }
        if (!Double.isFinite(gamma) || gamma < 0.0 || gamma > 1.0) {
            throw new IllegalArgumentException("Gamma debe ser una probabilidad entre 0 y 1.");
        }
    }
}
