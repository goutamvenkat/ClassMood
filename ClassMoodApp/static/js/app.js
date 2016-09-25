'use strict';

/* Angular Class Mood module config */

var app = angular.module('ClassMoodApp', ['ngRoute']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('//').endSymbol('//');

});

app.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when( "/", {
			templateUrl: '/templates/authentication/login.html'
		})
        .when("/classList", {
            templateUrl: "/templates/studentView/classList.html"
        });

		$locationProvider.html5Mode(true);
	}])
;