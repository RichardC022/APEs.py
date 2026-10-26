package model;

public class Individuo {
    private final int id;
    private Estado estado;

    public Individuo(int id, Estado estadoInicial) {
        if (id < 0) {
            throw new IllegalArgumentException("El identificador no puede ser negativo.");
        }
        if (estadoInicial == null) {
            throw new IllegalArgumentException("El estado no puede ser null.");
        }
        this.id = id;
        this.estado = estadoInicial;
    }

    public int getId() {
        return id;
    }

    public Estado getEstado() {
        return estado;
    }

    public void infectar() {
        if (estado != Estado.SUSCEPTIBLE) {
            throw new IllegalStateException("Solo un susceptible puede infectarse.");
        }
        estado = Estado.INFECTADO;
    }

    public void recuperar() {
        if (estado != Estado.INFECTADO) {
            throw new IllegalStateException("Solo un infectado puede recuperarse.");
        }
        estado = Estado.RECUPERADO;
    }
}
