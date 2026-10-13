Feature: Complete Authentication Flow
  As a user of the Six Flags app
  I want to verify email and password authentication scenarios
  So that I can log in securely or see appropriate validation errors

  @android @ios @login @regression
  Scenario: Login flow
    Given the user launches the app and navigates to the email screen
    When the user verifies all email screen UI elements and text
    When the user enters an invalid email "tha" and verifies the error message
    When the user enters a valid email "thangavel@tuna.group" and submits
    Then the user verifies all password screen UI elements and displayed email
    When the user enters an invalid password "invalid123" and verifies the error message
    When the user enters a valid password "Maya123@" and submits
    Then the user verifies the home screen is displayed via the manage account button


  @android @ios @login @smoke
  Scenario: Login flow
    Given the user launches the app and navigates to the email screen
    When the user enters a valid email "thangavel@tuna.group" and submits
    Then the user verifies all password screen UI elements and displayed email
    When the user enters a valid password "Maya123@" and submits
    Then the user verifies the home screen is displayed via the manage account button


  @android @ios @login @sanity
  Scenario: Login flow
    Given the user launches the app and navigates to the email screen
    When the user enters a valid email "thangavel@tuna.group" and submits
    When the user enters a valid password "Maya123@" and submits
    Then the user verifies the home screen is displayed via the manage account button








