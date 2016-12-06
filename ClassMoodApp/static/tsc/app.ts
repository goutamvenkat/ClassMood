///////////////////////////////////////////////////
//
// This file would handle routing if Angular were
// also used for the backend. This is handled by
// Flask.
//
///////////////////////////////////////////////////
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export var app: ng.IModule = angular.module("ClassMoodApp", ["ngRoute", "ngMaterial", "ui.bootstrap"]);
    
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
        })
        .when("/liveView", {
            templateUrl: "/templates/liveView.html"
        })
        .when("/lectureList/:classId", {
            templateUrl: "templates/lectureList.html",
            controller: "LectureListController"
        })
        .when("/pollingQuestionList/:class_id/:lecture_id", {
            templateUrl: "templates/pollingQuestionList.html",
            controller: "PollingQuestionListController"
        })
        .when("/pollingQuestionList/:class_id/:lecture_id/createPollingQuestion", {
            templateUrl: "templates/createPollingQuestion.html",
            controller: "CreatePollingQuestionController"
        });

		$locationProvider.html5Mode(true);
	}]);


}