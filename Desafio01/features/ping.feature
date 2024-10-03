Feature: API Ping
  Scenario: Verifica disponibilidad
    When hago ping a la API
    Then debería recibir una respuesta OK