package br.com.flightOnTime.service;


import br.com.flightOnTime.dto.PredictionHistoryDTO;
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
import java.util.List;
import java.util.stream.Collectors;


@Service
    public class PredictionService {

    private  final PredictionRepository predictionRepository;

        private final WebClient webClient;

        @Value("${api.python.endpoint:/predict_internal}")
        private String predictEndpoint;


        public PredictionService(WebClient.Builder webClientBuilder,PredictionRepository predictionRepository,
                                 @Value("${api.python.url:http://localhost:5000}") String pythonApiUrl) {
            this.webClient = webClientBuilder
                    .baseUrl(pythonApiUrl)
                    .build();
            this.predictionRepository = predictionRepository;
        }

        public PredictionResponseDTO getPrediction(PredictionRequestDTO request) {

            PredictionResponseDTO response = webClient.post()
                    .uri(predictEndpoint)
                    .bodyValue(request)
                    .retrieve()
                    .onStatus(status -> status.isError(),
                            clientResponse -> Mono.error(new PrevisaoNaoEncontrada("API Python offline ou erro no modelo")))
                    .bodyToMono(PredictionResponseDTO.class)
                    .block();


            if (response != null) {
                PredictionEntity entity = new PredictionEntity();
                entity.setOrigem(request.getOrigem());
                entity.setDataPartida(request.getData_partida());
                entity.setDistanciaKm(request.getDistancia_km());
                entity.setResultadoPrevisao(response.getPrevisao());
                entity.setProbabilidade(response.getProbabilidade());
                entity.setDataConsulta(LocalDateTime.now());
                predictionRepository.save(entity);
            }


            return response;
        }

/*
    public List<PredictionHistoryDTO> getHistory() {
        return predictionRepository.findAll().stream()
                .map(entity -> new PredictionHistoryDTO(
                        entity.getId(),
                        entity.getOrigem(),
                        entity.getDataPartida(),
                        entity.getResultadoPrevisao(),
                        entity.getProbabilidade(),
                        entity.getDataConsulta()
                )).toList();
           
    }

 */
    }

