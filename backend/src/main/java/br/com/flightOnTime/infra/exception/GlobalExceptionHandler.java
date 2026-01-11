package br.com.flightOnTime.infra.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;

@RestControllerAdvice
public class GlobalExceptionHandler {

       @ExceptionHandler(PredictionNotFound.class)
       public ResponseEntity<ErroResponseDTO> tratarPrevisaoNaoEncontrada(PredictionNotFound ex) {
            ErroResponseDTO erro = new ErroResponseDTO(ex.getMessage());
            return ResponseEntity
                    .status(HttpStatus.NOT_FOUND)
                    .body(erro);
        }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErroResponseDTO> handleGenericException(
            Exception ex) {

        ErroResponseDTO erro = new ErroResponseDTO(
                "Internal server error"
        );

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(erro);
    }


    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<List<ValidationErrors>> handleValidationErrors(
            MethodArgumentNotValidException ex) {

        var errors = ex.getFieldErrors()
                .stream()
                .map(ValidationErrors::new)
                .toList();

        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(errors);
    }}

