package br.com.flightOnTime.infra;

import br.com.flightOnTime.dto.ErroResponseDTO;
import br.com.flightOnTime.exception.PrevisaoNaoEncontrada;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ExcecoesGlobais {

       @ExceptionHandler(PrevisaoNaoEncontrada.class)
        public ResponseEntity<ErroResponseDTO> tratarPrevisaoNaoEncontrada(PrevisaoNaoEncontrada ex) {

            ErroResponseDTO erro = new ErroResponseDTO(ex.getMessage());

            return ResponseEntity
                    .status(HttpStatus.NOT_FOUND)
                    .body(erro);
        }
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErroResponseDTO> tratarIllegalArgument(IllegalArgumentException ex) {

        ErroResponseDTO erro = new ErroResponseDTO(ex.getMessage());

        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(erro);
    }
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErroResponseDTO> tratarErroGenerico(Exception ex) {

        ErroResponseDTO erro =
                new ErroResponseDTO("Erro interno no servidor");

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(erro);
    }
}


