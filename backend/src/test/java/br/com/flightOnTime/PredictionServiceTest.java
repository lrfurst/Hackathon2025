package br.com.flightOnTime;

import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.entity.PredictionEntity;
import br.com.flightOnTime.exception.PrevisaoNaoEncontrada;
import br.com.flightOnTime.repository.PredictionRepository;
import br.com.flightOnTime.service.PredictionService;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.*;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.function.client.WebClient;
import static org.junit.jupiter.api.Assertions.*;
import java.io.IOException;


import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;

@SpringBootTest
class PredictionServiceTest {

	@Mock
	private PredictionRepository predictionRepository; // Importe o org.mockito.Mock

	private static MockWebServer mockWebServer;
	private PredictionService predictionService; // Corrigido o erro de digitação (Servie -> Service)

	@BeforeAll
	static void setUp() throws IOException {
		mockWebServer = new MockWebServer();
		mockWebServer.start();
	}

	@AfterAll
	static void tearDown() throws IOException {
		mockWebServer.shutdown();
	}

	@BeforeEach
	void initialize() {
		MockitoAnnotations.openMocks(this);
		// Pegamos a URL dinâmica gerada pelo MockWebServer
		String baseUrl = mockWebServer.url("/").toString();

		WebClient.Builder webClientBuilder = WebClient.builder();

		// CORREÇÃO: Atribuímos à variável da classe definida na linha 17
		this.predictionService = new PredictionService(webClientBuilder,predictionRepository, baseUrl);

		// Como estamos usando 'new', o Spring não injeta o @Value automaticamente.
		// Usamos ReflectionTestUtils para simular a injeção do endpoint.
		ReflectionTestUtils.setField(predictionService, "predictEndpoint", "/predict_internal");
	}

@Test
@DisplayName("Deve retornar a previsão com sucesso e salvar no banco")
void getPrediction_Success() {
	// 1. GIVEN (Preparação)
	mockWebServer.enqueue(new MockResponse()
			.setResponseCode(200)
			.setBody("{\"previsao\": \"Pontual\", \"probabilidade\": 0.92}")
			.addHeader("Content-Type", "application/json"));

	// Configura o Mock do Banco de Dados ANTES da execução
	Mockito.when(predictionRepository.save(any(PredictionEntity.class)))
			.thenAnswer(i -> i.getArguments()[0]);

	PredictionRequestDTO request = new PredictionRequestDTO();
	request.setOrigem("GRU");
	request.setData_partida("2025-12-25T10:00:00");
	request.setDistancia_km(450); // Não esqueça do campo novo!

	// 2. WHEN (Execução)
	PredictionResponseDTO response = predictionService.getPrediction(request);

	// 3. THEN (Verificações)
	assertNotNull(response);
	assertEquals("Pontual", response.getPrevisao());
	assertEquals(0.92, response.getProbabilidade());

	// VERIFICAÇÃO EXTRA: Garante que o método save() foi chamado exatamente 1 vez
	// Isso prova que sua integração com o banco está funcionando no Service!
	Mockito.verify(predictionRepository, Mockito.times(1)).save(any(PredictionEntity.class));
}
	@Test
	@DisplayName("Deve lançar PrevisaoNaoEncontrada quando o Python retorna erro 4xx ou 5xx")
	void getPrediction_ApiError() {
		// GIVEN
		mockWebServer.enqueue(new MockResponse().setResponseCode(404));

		PredictionRequestDTO request = new PredictionRequestDTO();
		request.setOrigem("GIG");

		// WHEN & THEN
		assertThrows(PrevisaoNaoEncontrada.class, () -> {
			predictionService.getPrediction(request);
		});
	}
}
