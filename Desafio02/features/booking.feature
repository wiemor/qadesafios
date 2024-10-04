Feature: Booking App
  Scenario: Booking correcto
    Given estoy en el home
    When busco hoteles en "Cusco"
    And selecciono el segundo hotel disponible
    Then deberia ver el estado del booking
