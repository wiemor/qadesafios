Feature: API Booking

  Scenario: Crear una booking
    Given tengo detalles validos de booking
    When creo una booking
    Then deberia recibir una confirmacion de booking

  Scenario: Obtener detalles de una booking
    Given tengo un ID de booking valido
    When obtengo los detalles de la booking
    Then deberia ver la informacion correcta de la booking

  Scenario: Actualizar una booking
    Given tengo un token valido
    Given tengo un ID de booking valido
    And tengo nuevos detalles de booking
    When actualizo la booking
    Then deberia ver la informacion actualizada de la booking

  Scenario: Eliminar una booking
    Given tengo un token valido
    Given tengo un ID de booking valido
    When elimino la booking
    Then la booking deberia ser eliminada con exito

  Scenario: Intentar crear una booking con datos inválidos
    Given tengo detalles invalidos de booking
    When intento crear una booking
    Then deberia recibir un error de validacion

