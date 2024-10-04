Feature: Booking App
  Scenario: Booking correcto
    Given estoy en el home
    When busco hoteles en Cusco
    And selecciono el primer hotel disponible
    And completo el proceso de booking
    Then deberia ver la confirmación
