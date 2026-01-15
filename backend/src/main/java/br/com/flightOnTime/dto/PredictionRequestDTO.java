package br.com.flightOnTime.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
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
    @NotBlank(message = "O campo 'hora_dia' (manha, tarde, noite) é obrigatório.")
    @JsonProperty("hora_dia")
    private String horaDia;
    @NotNull(message = "O campo 'dia_semana' (1-7) é obrigatório.")
    @JsonProperty("dia_semana")
    private int diaSemana;


}

