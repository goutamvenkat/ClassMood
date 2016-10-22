declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export var app: ng.IModule = angular.module("ClassMoodApp", ["ngRoute", "ngMaterial"]);
    
    app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });

    app.config(['$routeProvider', '$locationProvider', 
            ($routeProvider, $locationProvider) => {
		$routeProvider
		.when( "/", {
			templateUrl: '/templates/authentication/login.html'
		})
        .when("/classList", {
            templateUrl: "/templates/classList.html"
        });

		$locationProvider.html5Mode(true);
	}]);
}