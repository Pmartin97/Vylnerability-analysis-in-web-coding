angular
  .module('app', ['angular-jwt'])
  .config(function Config($httpProvider, jwtOptionsProvider) {
    jwtOptionsProvider.config({
      whiteListedDomains: [/^api-version-\d+\.myapp\.com$/i, 'localhost']
    });
  });


