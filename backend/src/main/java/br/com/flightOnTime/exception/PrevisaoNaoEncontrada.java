package br.com.flightontime.exception;

public class PrevisaoNaoEncontrada extends RuntimeException {
    public PrevisaoNaoEncontrada(String message) {
        super(message);
    }
    
    public PrevisaoNaoEncontrada(String message, Throwable cause) {
        super(message, cause);
    }
}
