# Created by Hema at 5/19/2017
Feature: Dashboard Page

  Scenario: No Watchlists Initially
    Given a user visits the site
    Then she should see Coin mart
    Then she should not see any watchlists

  Scenario: See Watchlists
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "Test" and password "Test_123"
    Then she should see her list of watchlists

  Scenario: See Watchlists With Current Value
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "Test" and password "Test_123"
    Then she should see her list of watchlists with current value

  Scenario: See Watchlists With Historical Value
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "Test" and password "Test_123"
    Then she should see her list of watchlists with historical value
