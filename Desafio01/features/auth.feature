Feature: API Auth
  Scenario: Autenticacion valida
    Given que tengo credenciales validas
    When me autentico en la API con credenciales validas
    Then deberia recibir un token valido

  Scenario: Autenticacion invalida
    Given que tengo credenciales invalidas
    When me autentico en la API con credenciales invalidas
    Then deberia recibir un mensaje de error