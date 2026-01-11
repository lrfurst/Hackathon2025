package br.com.flightOnTime.infra.exception;

public class PredictionNotFound extends RuntimeException {
    public PredictionNotFound(String message) {
        super(message);
    }
}
