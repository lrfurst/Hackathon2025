package br.com.flightOnTime.entity;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name="predict")
@AllArgsConstructor
@NoArgsConstructor
@Data
public class PredictionEntity {


    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 10)
    private String companhia;

    @Column(nullable = false, length = 10)
    private String origem;

    @Column(nullable = false, length = 10)
    private String destino;

    @Column(name = "hora_dia", nullable = false, length = 10)
    private String horaDia; // manha | tarde | noite

    @Column(name = "dia_semana", nullable = false)
    private Integer diaSemana; // 1 a 7

    @Column(name = "data_partida", nullable = false)
    private String dataPartida;

    @Column(name = "distancia_km", nullable = false)
    private Integer distanciaKm;

    @Column(name = "resultado_previsao", nullable = false, length = 20)
    private String resultadoPrevisao;

    @Column(nullable = false)
    private Double probabilidade;

    @Column(name = "data_consulta", nullable = false)
    private LocalDateTime dataConsulta;


}
