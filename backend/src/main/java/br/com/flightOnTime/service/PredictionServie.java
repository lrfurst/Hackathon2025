package br.com.flightOnTime.service;


import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.exception.PrevisaoNaoEncontrada;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class PredictionServie {
    // Endereço do microserviço Python (porta 5000)
    private final String PYTHON_API_URL = "http://localhost:5000"; // URL base
    private final String PREDICT_ENDPOINT = "/predict_internal"; // Endpoint específico
    private final WebClient webClient;

    public PredictionServie(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
                .baseUrl(PYTHON_API_URL)
                .build();
    }

    public PredictionResponseDTO getPrediction(PredictionRequestDTO request) {

        // 1. Chama a API Python (POST para http://localhost:5000/predict_internal)
        return webClient.post()
                .uri(PREDICT_ENDPOINT)
                .bodyValue(request) // Envia o objeto FlightRequest como corpo JSON
                .retrieve()
                // 2. Tratamento de Erros da Chamada HTTP (4xx e 5xx)
                .onStatus(status -> status.is4xxClientError() || status.is5xxServerError(),
                        response -> Mono.error(new PrevisaoNaoEncontrada("Erro ao chamar o serviço de previsão Python: Código " + response.statusCode())))

                // 3. Mapeia a Resposta JSON para o objeto Java PredictionResponse
                .bodyToMono(PredictionResponseDTO.class)
                .block(); // Bloqueia para obter o resultado (simples para MVP)
    }
}
