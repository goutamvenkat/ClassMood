/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var LiveViewController = (function () {
        function LiveViewController($scope, $http, $timeout) {
            this.$scope = $scope;
            this.$http = $http;
            this.$timeout = $timeout;
            this.$http = $http;
            this.$scope = $scope;
            this.getIsStudent();
            this.getUserId();
            this.getLectureId();
            this.gauge = new ClassMoodApp.GaugeModel();
            this.gauge.depth_num = 0;
            this.gauge.pace_num = 0;
        }
        LiveViewController.prototype.getUserId = function () {
            var _this = this;
            this.$http.get('/user_id').then(function (response) {
                _this.userId = response.data.results;
            });
        };
        LiveViewController.prototype.getIsStudent = function () {
            var _this = this;
            this.$http.get("/is_student").success(function (is_student, status) {
                _this.isStudent = is_student.results;
                if (!_this.isStudent) {
                    _this.gaugePollPace(_this);
                    _this.gaugePollDepth(_this);
                }
                else {
                    _this.getGauge(_this);
                }
            });
        };
        LiveViewController.prototype.getLectureId = function () {
            this.lectureId = parseInt($("#lectureId").attr('lecture-id'), 10);
        };
        LiveViewController.prototype.votePace = function (newPace) {
            this.gauge.pace_num = newPace;
            this.postCurrentGauge();
        };
        LiveViewController.prototype.voteDepth = function (newDepth) {
            this.gauge.depth_num = newDepth;
            this.postCurrentGauge();
        };
        LiveViewController.prototype.getGauge = function (self) {
            self.$http.get("/live_lecture/gauge/get/" + self.lectureId)
                .success(function (response) {
                self.gauge.pace_num = response.results[0];
                if (self.gauge.pace_num == -1) {
                    var pace = $("#pace1");
                    $("#pace1").prop('checked', true);
                    $("#pace1").parent().addClass('active');
                }
                else if (self.gauge.pace_num == 1) {
                    $("#pace3").prop('checked', true);
                    $("#pace3").parent().addClass('active');
                }
                else {
                    $("#pace2").prop('checked', true);
                    $("#pace2").parent().addClass('active');
                }
                self.gauge.depth_num = response.results[1];
                if (self.gauge.depth_num == -1) {
                    $("#depth1").prop('checked', true);
                    $("#depth1").parent().addClass('active');
                }
                else if (self.gauge.depth_num == 1) {
                    $("#depth3").prop('checked', true);
                    $("#depth3").parent().addClass('active');
                }
                else {
                    $("#depth2").prop('checked', true);
                    $("#depth2").parent().addClass('active');
                }
            })
                .error(function (response) {
            });
        };
        LiveViewController.prototype.postCurrentGauge = function () {
            this.$http.post('/live_lecture/gauge/update', JSON.stringify({ lect_id: this.lectureId, pace_num: this.gauge.pace_num, depth_num: this.gauge.depth_num }))
                .success(function (data, status, headers, config) {
            })
                .error(function (data, status, header, config) {
                console.log("ERROR while posting current gauge");
            });
        };
        LiveViewController.prototype.gaugePollPace = function (self) {
            this.$http.get("/live_lecture/pace/get/" + this.lectureId)
                .success(function (response) {
                self.gauge.pace_num = response;
                $('#paceSlider').get(0).MaterialSlider.change(self.gauge.pace_num);
                self.$timeout(function () { self.gaugePollPace(self); }, 5000);
            })
                .error(function (response) {
                self.$timeout(function () { self.gaugePollPace(self); }, 10000);
            });
        };
        LiveViewController.prototype.gaugePollDepth = function (self) {
            this.$http.get("/live_lecture/depth/get/" + this.lectureId)
                .success(function (response) {
                self.gauge.depth_num = response;
                $('#depthSlider').get(0).MaterialSlider.change(self.gauge.depth_num);
                self.$timeout(function () { self.gaugePollDepth(self); }, 5000);
            })
                .error(function (response) {
                self.$timeout(function () { self.gaugePollDepth(self); }, 10000);
            });
        };
        LiveViewController.$inject = ["$scope", "$http", "$timeout"];
        return LiveViewController;
    }());
    ClassMoodApp.LiveViewController = LiveViewController;
    ClassMoodApp.app.controller('LiveViewController', LiveViewController);
})(ClassMoodApp || (ClassMoodApp = {}));
