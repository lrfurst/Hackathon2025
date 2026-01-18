package br.com.flightOnTime.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PredictionResponseDTO {
    @JsonProperty("resultadoPrevisao")
    @JsonAlias("prediction")
    private Integer previsao;

    @JsonProperty("probabilidade")
    @JsonAlias("probability")
    private Double probabilidade;

    @JsonProperty("custoEvitado")
    @JsonAlias("avoided_cost")
    private Double custoEvitado;
}
