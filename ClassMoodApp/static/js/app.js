'use strict';

/* Angular Class Mood module config */
var app = angular.module('ClassMoodApp', ['ngRoute']);
app.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when( "/", {
			templateUrl: '/templates/authentication/login.html'
		});

		$locationProvider.html5Mode(true);
	}])
;