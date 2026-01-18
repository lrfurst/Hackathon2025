package br.com.flightOnTime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PredictionRequestDTO {

    @NotBlank(message = "O campo 'companhia' é obrigatório.")
    private String companhia;

    @NotBlank(message = "O campo 'origem' é obrigatório.")
    @JsonProperty("aeroporto_origem")
    private String origem;

    @NotBlank(message = "O campo 'destino' é obrigatório.")
    @JsonProperty("aeroporto_destino")
    private String destino;

    @NotBlank
    @JsonProperty("data_partida")
    private String dataPartida;

    @Positive(message = "A distância deve ser um valor positivo.")
    @JsonProperty("distancia")
    private Integer distanciaKm;

    @NotBlank(message = "O campo 'hora_dia' (manha, tarde, noite) é obrigatório.")
    @JsonProperty("hora_partida")
    private String horaDia;

    @NotNull(message = "O campo 'dia_semana' (1-7) é obrigatório.")
    @JsonProperty("dia_semana")
    private Integer diaSemana;


}

