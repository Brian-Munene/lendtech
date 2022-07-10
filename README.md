# Lending Application

The system enables users to register and login upon registration a bankAccount is created within the system. This will store the user's balance and be used to transact with other users in the system.

There is a get profile endpoint [Profile](https://lendttech.herokuapp.com/accounts/profile) that returns the user's details such as bankAccount information and registration details for a loggedIn user.

## Loans

### How to get a Loan

Once a user is loggedIn they can get a loan by making a POST request to [Get Loan](https://lendttech.herokuapp.com/loans/) with
```
{
    borrower: borrower_bank_account_id,
    amount: amount 
 }
```

### How to view all loans
Visit [View loans](https://lendttech.herokuapp.com/loans/) after logging ing.

### Filtering Loans by date

Filtering uses a date range to display all the loans received between the two dates.

To view filtered loans visit [Filtered Loans](https://lendttech.herokuapp.com/loans/?start_date=2022-07-09&end_date=2022-07-09)
To change the date range simply edit the start_date and end_date in the url to a date of your choice.

## Payments

### Making a payment

A loggedIn user can make a payment to another account in the system by making a POST request to [Make a Payment](https://lendttech.herokuapp.com/payments/) with 
```
{
    payer: payer_bank_account_id
    payee: payee_bank_account_id,
    amount: 1000.00
 }
```

### Viewing a Payments

A loggedIn user can view payments using [View Payments](https://lendttech.herokuapp.com/payments/)

## How to Test

To run the tests first set up the project on your local machine as you would set up a normal Django project.
Inside your virtual environment use the command  ```python manage.py test --with-coverage``` to run all tests and show the coverage report of the tests in the application.
