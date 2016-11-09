/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export class LoginViewController {
        static $inject = ["$scope", "$http", "$window"];
        constructor(private $scope: ng.IScope,
                    // private $auth,
                    private $http: ng.IHttpService,
                    private $window: ng.IWindowService) {
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


        public onSignIn(googleUser): void {
            // this.$window.onSignIn = onSignIn(googleUser) {
                // var profile = googleUser.getBasicProfile();
                // console.log('ID: ' + profile.getId());
                // console.log('Name: ' + profile.getName());
                // console.log('Image URL: ' + profile.getImageUrl());
                // console.log('Email: ' + profile.getEmail());
            // }
        }
        
    }
    app.controller('LoginViewController', LoginViewController);
}