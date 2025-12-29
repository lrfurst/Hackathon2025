package br.com.flightOnTime;

import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.exception.PrevisaoNaoEncontrada;
import br.com.flightOnTime.service.PredictionService;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.*;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.web.reactive.function.client.WebClient;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class FlightOnTimeJavaApplicationTests {
	private static MockWebServer mockWebServer;
	private PredictionService predictionServie;

	@BeforeAll
	static void setUp() throws IOException {
		mockWebServer = new MockWebServer();
		// Iniciamos na porta 5000 para coincidir com a URL fixa no seu Service
		mockWebServer.start(5000);
	}

	@AfterAll
	static void tearDown() throws IOException {
		mockWebServer.shutdown();
	}

	@BeforeEach
	void initialize() {
		// O Spring injetaria isso, aqui fazemos manualmente para o teste
		WebClient.Builder webClientBuilder = WebClient.builder();
		predictionServie = new PredictionService(webClientBuilder);
	}

	@Test
	@DisplayName("Deve retornar a previsão com sucesso quando o Python responde 200 OK")
	void getPrediction_Success() {
		// GIVEN: Preparamos o servidor para devolver um JSON de sucesso
		mockWebServer.enqueue(new MockResponse()
				.setResponseCode(200)
				.setBody("{\"previsao\": \"Pontual\", \"probabilidade\": 0.92}")
				.addHeader("Content-Type", "application/json"));

		PredictionRequestDTO request = new PredictionRequestDTO();
		request.setOrigem("GRU");
		request.setData_partida("2025-12-25T10:00:00");

		// WHEN: Chamamos o método do serviço
		PredictionResponseDTO response = predictionServie.getPrediction(request);

		// THEN: Verificamos se os dados foram mapeados corretamente
		assertNotNull(response);
		assertEquals("Pontual", response.getPrevisao());
		assertEquals(0.92, response.getProbabilidade());
	}

	@Test
	@DisplayName("Deve lançar PrevisaoNaoEncontrada quando o Python retorna erro 4xx ou 5xx")
	void getPrediction_ApiError() {
		// GIVEN: Servidor simulando um erro 404
		mockWebServer.enqueue(new MockResponse().setResponseCode(404));

		PredictionRequestDTO request = new PredictionRequestDTO();
		request.setOrigem("GIG");

		// WHEN & THEN: Verificamos se a exceção personalizada é lançada
		assertThrows(PrevisaoNaoEncontrada.class, () -> {
			predictionServie.getPrediction(request);
		});
	}

}
