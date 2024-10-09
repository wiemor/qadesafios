Feature: API Auth
  Scenario: Valid authentication
    Given I have valid credentials
    When I authenticate in the API with valid credentials
    Then I should receive a valid token

  Scenario: Invalid authentication
    Given I have invalid credentials
    When I authenticate in the API with invalid credentials
    Then I should receive an error message