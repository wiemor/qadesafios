Feature: API Ping
  Scenario: Check availability
    Given: That the API is up and running
    When I ping the API
    Then I should get an OK response