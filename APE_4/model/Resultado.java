package model;

public final class Resultado {
    private final int tiempo;
    private final int susceptibles;
    private final int infectados;
    private final int recuperados;

    public Resultado(int tiempo, int susceptibles, int infectados, int recuperados) {
        if (tiempo < 0) {
            throw new IllegalArgumentException("El tiempo no puede ser negativo.");
        }
        if (susceptibles < 0 || infectados < 0 || recuperados < 0) {
            throw new IllegalArgumentException("Los contadores de estados no pueden ser negativos.");
        }
        this.tiempo = tiempo;
        this.susceptibles = susceptibles;
        this.infectados = infectados;
        this.recuperados = recuperados;
    }

    public int getTiempo() {
        return tiempo;
    }

    public int getSusceptibles() {
        return susceptibles;
    }

    public int getInfectados() {
        return infectados;
    }

    public int getRecuperados() {
        return recuperados;
    }

    public String toCSV() {
        return tiempo + "," + susceptibles + "," + infectados + "," + recuperados;
    }
}
