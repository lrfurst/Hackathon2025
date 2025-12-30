package br.com.flightOnTime.service;


import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.entity.PredictionEntity;
import br.com.flightOnTime.exception.PrevisaoNaoEncontrada;
import br.com.flightOnTime.repository.PredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;


@Service
    public class PredictionService {

    private  final PredictionRepository predictionRepository;

        private final WebClient webClient;

        // Injetamos o endpoint via @Value. Se não houver no properties, ele usa o padrão definido após os ':'
        @Value("${api.python.endpoint:/predict_internal}")
        private String predictEndpoint;

        // Construtor: Spring injeta o Builder e a URL definida no application.properties
        public PredictionService(WebClient.Builder webClientBuilder,PredictionRepository predictionRepository,
                                 @Value("${api.python.url:http://localhost:5000}") String pythonApiUrl) {
            this.webClient = webClientBuilder
                    .baseUrl(pythonApiUrl)
                    .build();
            this.predictionRepository = predictionRepository;
        }

        public PredictionResponseDTO getPrediction(PredictionRequestDTO request) {
            // 1. Fazemos a chamada e guardamos o resultado na variável 'response'
            PredictionResponseDTO response = webClient.post()
                    .uri(predictEndpoint)
                    .bodyValue(request)
                    .retrieve()
                    .onStatus(status -> status.isError(),
                            clientResponse -> Mono.error(new PrevisaoNaoEncontrada("API Python offline ou erro no modelo")))
                    .bodyToMono(PredictionResponseDTO.class)
                    .block();

            // 2. Agora que temos a 'response', salvamos no banco
            if (response != null) {
                PredictionEntity entity = new PredictionEntity();

                // Dados do Request (Usuário)
                entity.setOrigem(request.getOrigem());
                entity.setDataPartida(request.getData_partida());
                entity.setDistanciaKm(request.getDistancia_km());

                // Dados do Response (IA Python)
                entity.setResultadoPrevisao(response.getPrevisao());
                entity.setProbabilidade(response.getProbabilidade());

                // Timestamp da consulta
                entity.setDataConsulta(LocalDateTime.now());

                predictionRepository.save(entity);
            }

            // 3. Por fim, retornamos a resposta para o Controller
            return response;
        }
    }

