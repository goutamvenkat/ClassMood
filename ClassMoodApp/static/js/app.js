var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    ClassMoodApp.app = angular.module("ClassMoodApp", ["ngRoute", "ngMaterial", "ui.bootstrap"]);
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
})(ClassMoodApp || (ClassMoodApp = {}));
