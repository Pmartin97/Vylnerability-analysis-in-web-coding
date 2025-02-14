var app = angular.module('app', []);
var expressions = require("angular-expressions");
 
evaluate = expressions.compile("1 + 1");



app.controller('MyCtrl', function ($scope) {

    var coreObject = {
        name: 'test merge',
        settings: {
            server: {
                Url: 'www.google.com'
            }
        }
    }

    $scope.sourceObject = angular.copy(coreObject);
    $scope.extend = function () {
        var objectWithSettings = {
            name: 'overriden name',
            settings: {
                open: true,
                close: false,
                server: {
                    Url: 'localhost:5999'
                }
            }
        }
        console.log(evaluate());
        angular.merge($scope.sourceObject, objectWithSettings);
    }
});
