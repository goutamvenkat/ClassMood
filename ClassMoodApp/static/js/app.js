var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    ClassMoodApp.app = angular.module("ClassMoodApp", ["ngRoute", "ngMaterial"]);
    ClassMoodApp.app.config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });
    ClassMoodApp.app.config(['$routeProvider', '$locationProvider',
        function ($routeProvider, $locationProvider) {
            $routeProvider
                .when("/", {
                templateUrl: '/templates/authentication/login.html'
            })
                .when("/classList", {
                templateUrl: "/templates/classList.html"
            })
                .when("/liveView", {
                templateUrl: "/templates/liveView.html"
            });
            $locationProvider.html5Mode(true);
        }]);
})(ClassMoodApp || (ClassMoodApp = {}));
