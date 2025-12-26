package br.com.flightOnTime.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PredictionRequestDTO {

    private String companhia;
    private String origem;
    private String destino;
    private String data_partida;
    private int distancia_km;

}

