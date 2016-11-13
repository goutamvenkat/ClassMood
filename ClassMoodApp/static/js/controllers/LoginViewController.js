/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var LoginViewController = (function () {
        function LoginViewController($scope, 
            // private $auth,
            $http, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$window = $window;
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            // this.$auth = $auth;
        }
        // public authenticate(provider): void {
        //     this.$auth.authenticate(provider).then(
        //         (response) => {
        //             console.log('SUCCESSFUL AUTH ' + response);
        //         }
        //     ).catch((response) => {
        //             console.log('UNSUCCESSFUL AUTH ' + response);
        //         });
        // }
        LoginViewController.prototype.onSignIn = function (googleUser) {
            // this.$window.onSignIn = onSignIn(googleUser) {
            // var profile = googleUser.getBasicProfile();
            // console.log('ID: ' + profile.getId());
            // console.log('Name: ' + profile.getName());
            // console.log('Image URL: ' + profile.getImageUrl());
            // console.log('Email: ' + profile.getEmail());
            // }
        };
        LoginViewController.$inject = ["$scope", "$http", "$window"];
        return LoginViewController;
    }());
    ClassMoodApp.LoginViewController = LoginViewController;
    ClassMoodApp.app.controller('LoginViewController', LoginViewController);
})(ClassMoodApp || (ClassMoodApp = {}));
