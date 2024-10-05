Feature: Booking App
  Scenario: Booking correcto
    Given estoy en el home
    When busco hoteles en "Cusco"
    And selecciono el segundo hotel disponible
    And ingreso informacion personal
    And ingreso credit card information
    Then deberia ver el booking
