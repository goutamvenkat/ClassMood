/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var CreatePollingQuestionController = (function () {
        function CreatePollingQuestionController($scope, $http, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$window = $window;
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            var curLink = $window.location.pathname.split("/");
            this.classId = parseInt(curLink[curLink.length - 3]);
            this.lecture_id = parseInt(curLink[curLink.length - 2]);
        }
        CreatePollingQuestionController.prototype.submitPollingQuestion = function () {
            var _this = this;
            var text = this.question_text;
            var a = this.a_text;
            var b = this.b_text;
            var c = this.c_text;
            var d = this.d_text;
            var ans = this.ans;
            var options = [a, b, c, d];
            // Ignore option a because we check that it is not undefined later
            for (var i = 1; i < options.length; i++) {
                if (options[i] === undefined) {
                    options[i] = "";
                }
            }
            console.log(text + " " + a + " " + b + " " + c + " " + d + " " + ans);
            if (!this.isStudent) {
                if (text && a && ans.length != 0) {
                    this.$http.get("/create_polling_question/" + this.lecture_id + "/" + text + "/" + a + "/" + b + "/" + c + "/" + d + "/" + ans).then(function (response) {
                        if (response.data) {
                            _this.$window.location.href = "/pollingQuestionList/" + _this.classId + "/" + _this.lecture_id;
                        }
                    });
                }
                else {
                    window.alert("Please enter a question and at least one answer choice.");
                }
            }
        };
        CreatePollingQuestionController.$inject = ["$scope", "$http", "$window"];
        return CreatePollingQuestionController;
    }());
    ClassMoodApp.CreatePollingQuestionController = CreatePollingQuestionController;
    ClassMoodApp.app.controller('CreatePollingQuestionController', CreatePollingQuestionController);
})(ClassMoodApp || (ClassMoodApp = {}));
