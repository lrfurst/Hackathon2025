package br.com.flightOnTime;
import br.com.flightOnTime.controller.PredictionController;
import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.service.PredictionService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(PredictionController.class)
public class PredictionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private PredictionService predictionService; // "Mocamos" o service


    private ObjectMapper objectMapper; // Para converter objetos em JSON

    @BeforeEach
    void setUp() {
        // Inicializamos o ObjectMapper manualmente para garantir que ele tenha suporte a datas
        objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
    }

    @Test
    @DisplayName("Deve retornar 200 OK e o JSON de resposta ao receber dados válidos")
    void predict_Success() throws Exception {
        // GIVEN: Preparamos a resposta que o Service deve retornar
        PredictionResponseDTO mockResponse = new PredictionResponseDTO();
        mockResponse.setPrevisao("Pontual");
        mockResponse.setProbabilidade(0.85);

        Mockito.when(predictionService.getPrediction(any(PredictionRequestDTO.class)))
                .thenReturn(mockResponse);

        // Criamos o Request preenchendo TODOS os campos (ajuste conforme seu DTO real)
        PredictionRequestDTO request = new PredictionRequestDTO();
        request.setOrigem("GRU");
        request.setDestino("JFK"); // Exemplo de campo adicional
        request.setData_partida("2025-12-25T10:00:00");
        request.setCompanhia("LATAM"); // Exemplo de campo adicional
        request.setDistancia_km(450);
        // WHEN & THEN
        mockMvc.perform(post("/predict")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk()) // Agora o status deve ser 200
                .andExpect(jsonPath("$.previsao").value("Pontual"))
                .andExpect(jsonPath("$.probabilidade").value(0.85));
    }

    @Test
    @DisplayName("Deve retornar 400 Bad Request quando os dados de entrada forem inválidos")
    void predict_ValidationError() throws Exception {
        // GIVEN: Um objeto vazio que deve falhar no @Valid do Controller
        PredictionRequestDTO invalidRequest = new PredictionRequestDTO();

        // WHEN & THEN
        mockMvc.perform(post("/predict")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest());
    }


}
