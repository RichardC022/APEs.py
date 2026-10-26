import controller.ControladorSimulacion;

public class Main {
    public static void main(String[] args) {
        if (args.length > 1) {
            System.err.println("Uso: java Main [semilla]");
            System.exit(2);
        }

        long semilla = System.nanoTime();
        if (args.length == 1) {
            try {
                semilla = Long.parseLong(args[0]);
            } catch (NumberFormatException e) {
                System.err.println("La semilla debe ser un número entero largo.");
                System.exit(2);
            }
        }

        int poblacionTotal = 100;
        int infectadosIniciales = 5;
        double beta = 0.30;
        double gamma = 0.10;
        int pasosSimulacion = 100;

        System.out.println("Semilla utilizada: " + semilla);

        ControladorSimulacion controlador = new ControladorSimulacion(
                poblacionTotal, infectadosIniciales, beta, gamma,
                pasosSimulacion, semilla);

        if (!controlador.ejecutar()) {
            System.exit(1);
        }
    }
}
