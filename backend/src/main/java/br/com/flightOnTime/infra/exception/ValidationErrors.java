package br.com.flightOnTime.infra.exception;

import org.springframework.validation.FieldError;

public record ValidationErrors(String campo, String mensagem) {
    public ValidationErrors(FieldError erros){
        this(erros.getField(), erros.getDefaultMessage());
    }
}
