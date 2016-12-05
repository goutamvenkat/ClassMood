/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var CreatePollingQuestionController = (function () {
        function CreatePollingQuestionController($scope, $http, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$window = $window;
            this.question_text = '';
            this.a_text = '';
            this.b_text = '';
            this.c_text = '';
            this.d_text = '';
            this.ans = 'A';
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            var curLink = $window.location.pathname.split("/");
            this.classId = parseInt(curLink[curLink.length - 3]);
            this.lecture_id = parseInt(curLink[curLink.length - 2]);
        }
        CreatePollingQuestionController.prototype.submitPollingQuestion = function () {
            var _this = this;
            var text = encodeURIComponent(this.question_text);
            var a = encodeURIComponent(this.a_text);
            var b = encodeURIComponent(this.b_text);
            var c = encodeURIComponent(this.c_text);
            var d = encodeURIComponent(this.d_text);
            var ans = encodeURIComponent(this.ans);
            var url = "/create_polling_question/" + this.lecture_id + "/" + text + "/" + a + "/" + b + "/" + c + "/" + d + "/" + this.ans;
            console.log(text + " " + a + " " + b + " " + c + " " + d + " " + this.ans);
            if (!this.isStudent) {
                if (text && ans.length != 0) {
                    this.$http.get(url).then(function (response) {
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
