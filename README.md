# Vulnerability analysis in web coding

This application consist on a Javascript vulnerabilities detector. Although it is easy to install, it was deployed on Heroku.
The first time you try to access to the application it will be turn on before its test.
[Link to the application!](https://analyzer-tfg.herokuapp.com/accounts/login)

## How does it work?

First of all, the application makes a lexical analysis. After that it checks if there is any coincidence with one of the vulnerabilities in the database.
Finally, it saves the result in the database and creates an inform with the result.
