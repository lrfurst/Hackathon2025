package br.com.flightOnTime.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PredictionRequestDTO {

    @NotBlank(message = "não pode estar em branco.")
    private String companhia;
    @NotBlank(message = "não pode estar em branco.")
    private String origem;
    @NotBlank(message = "não pode estar em branco.")
    private String destino;
    @NotBlank(message = "não pode estar em branco.")
    private String data_partida;
    @NotBlank(message = "não pode estar em branco.")
    private int distancia_km;

}

