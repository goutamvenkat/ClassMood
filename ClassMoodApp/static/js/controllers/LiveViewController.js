/// <reference path="../app.ts" />
var ClassMoodApp;
(function (ClassMoodApp) {
    "use strict";
    var LiveViewController = (function () {
        function LiveViewController($scope, $http, $timeout, $window) {
            this.$scope = $scope;
            this.$http = $http;
            this.$timeout = $timeout;
            this.$window = $window;
            this.$http = $http;
            this.$scope = $scope;
            this.$window = $window;
            this.gauge = new ClassMoodApp.GaugeModel();
            this.gauge.depth_num = 0;
            this.gauge.pace_num = 0;
            this.questionEntered = '';
            this.studentResponse = 'A';
            this.questions = new ClassMoodApp.AnonymousQuestionsModel();
            this.questions.questions_array = [];
            this.questions.questions_string = '';
            this.currentPollingQuestion = 0;
            this.currentlyPresenting = false;
            this.pollingQuestionStudent = new ClassMoodApp.PollingQuestionStudentModel();
            this.pollingQuestionStudent.question_id = 0;
            this.pollingQuestionStudentExist = false;
        }
        LiveViewController.prototype.init = function (class_id, lecture_id, live_lecture_id) {
            this.classId = class_id;
            this.lectureId = lecture_id;
            this.liveLectureId = live_lecture_id;
            this.getIsStudent();
            this.getUserId();
        };
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
                    _this.pollAnonymousQuestions(_this);
                    _this.getPollingQuestions();
                }
                else {
                    _this.getGauge(_this);
                    _this.pollQuestionsStudent(_this);
                    _this.pollCurrentLiveLecture(_this);
                }
            });
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
            self.$http.get("/live_lecture/gauge/get/" + self.liveLectureId)
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
            this.$http.post('/live_lecture/gauge/update', JSON.stringify({ live_lect_id: this.liveLectureId, pace_num: this.gauge.pace_num, depth_num: this.gauge.depth_num }))
                .success(function (data, status, headers, config) {
            })
                .error(function (data, status, header, config) {
                console.log("ERROR while posting current gauge");
            });
        };
        LiveViewController.prototype.gaugePollPace = function (self) {
            this.$http.get("/live_lecture/pace/get/" + this.liveLectureId)
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
            this.$http.get("/live_lecture/depth/get/" + this.liveLectureId)
                .success(function (response) {
                self.gauge.depth_num = response;
                $('#depthSlider').get(0).MaterialSlider.change(self.gauge.depth_num);
                self.$timeout(function () { self.gaugePollDepth(self); }, 5000);
            })
                .error(function (response) {
                self.$timeout(function () { self.gaugePollDepth(self); }, 10000);
            });
        };
        LiveViewController.prototype.pollAnonymousQuestions = function (self) {
            this.$http.get("/live_lecture/questions/get/" + this.liveLectureId)
                .success(function (response) {
                console.log(response);
                self.questions.questions_array = response.results;
                self.questions.questions_string = self.questions.questions_array.join('\n');
                self.$timeout(function () { self.pollAnonymousQuestions(self); }, 5000);
            })
                .error(function (response) {
                self.$timeout(function () { self.pollAnonymousQuestions(self); }, 10000);
            });
        };
        LiveViewController.prototype.pollCurrentLiveLecture = function (self) {
            this.$http.get("/live_lecture/get_id/" + this.classId)
                .success(function (response) {
                if (response.live_lecture_id != self.liveLectureId) {
                    console.log("Live lecture changed or ended...");
                    self.$window.location.href = '/';
                }
                else {
                    console.log("Live lecture matches current");
                    self.$timeout(function () { self.pollCurrentLiveLecture(self); }, 15000);
                }
            })
                .error(function (response) {
                self.$timeout(function () { self.pollCurrentLiveLecture(self); }, 60000);
            });
        };
        LiveViewController.prototype.submitPressed = function () {
            this.submitAnonymousQuestion(this);
        };
        LiveViewController.prototype.submitAnonymousQuestion = function (self) {
            if (this.questionEntered !== '') {
                this.$http.get("/live_lecture/questions/put/" + this.liveLectureId + "/" + this.questionEntered)
                    .success(function (response) {
                    self.questions.questions_array.push(self.questionEntered);
                    self.questions.questions_string = self.questions.questions_array.join('\n');
                    self.questionEntered = '';
                });
            }
        };
        LiveViewController.prototype.resetGauges = function () {
            var _this = this;
            if (!this.isStudent) {
                this.$http.get("/reset_gauges/" + this.liveLectureId).success(function (data, status) {
                    if (data.results === true) {
                        _this.gaugePollPace(_this);
                        _this.gaugePollDepth(_this);
                    }
                }).catch(function (error) {
                    console.log(error);
                });
            }
        };
        LiveViewController.prototype.getPollingQuestions = function () {
            var self = this;
            this.$http.get("/get_polling_questions/" + this.lectureId)
                .success(function (response) {
                self.pollingQuestions = response.results;
                self.pollingQuestionResponses = [];
                if (self.pollingQuestions.length > 0) {
                    for (var i = 0; i < self.pollingQuestions.length; i++) {
                        var currentResponse = new ClassMoodApp.PollingQuestionResponseModel();
                        currentResponse.A = 0;
                        currentResponse.B = 0;
                        currentResponse.C = 0;
                        currentResponse.D = 0;
                        currentResponse.correct_answer = "";
                        currentResponse.num_responses = 0;
                        currentResponse.polled = false;
                        self.pollingQuestionResponses.push(currentResponse);
                    }
                    self.rebuildCurrentQuestion();
                }
            });
        };
        LiveViewController.prototype.previousPollingQuestion = function () {
            if (!this.currentlyPresenting) {
                this.currentPollingQuestion -= 1;
                if (this.currentPollingQuestion < 0) {
                    this.currentPollingQuestion = 0;
                }
                else {
                    this.rebuildCurrentQuestion();
                }
            }
        };
        LiveViewController.prototype.nextPollingQuestion = function () {
            if (!this.currentlyPresenting) {
                this.currentPollingQuestion += 1;
                if (this.currentPollingQuestion >= this.pollingQuestions.length) {
                    this.currentPollingQuestion = this.pollingQuestions.length - 1;
                }
                else {
                    this.rebuildCurrentQuestion();
                }
            }
        };
        LiveViewController.prototype.beginPresentingQuestion = function () {
            if (!this.currentlyPresenting) {
                var self = this;
                this.$http.get("/live_lecture/present_polling_question/get/" + this.liveLectureId + "/" + this.pollingQuestions[this.currentPollingQuestion].id)
                    .success(function (response) {
                    self.currentlyPresenting = true;
                });
            }
        };
        LiveViewController.prototype.stopPresentingQuestion = function () {
            if (this.currentlyPresenting) {
                var self = this;
                this.$http.get("/live_lecture/stop_polling_questions/" + this.liveLectureId)
                    .success(function (response) {
                    self.currentlyPresenting = false;
                    var responseStats = response[self.pollingQuestions[self.currentPollingQuestion].id];
                    if (responseStats != null) {
                        if (responseStats.A != null) {
                            self.pollingQuestionResponses[self.currentPollingQuestion].A = responseStats.A;
                        }
                        if (responseStats.B != null) {
                            self.pollingQuestionResponses[self.currentPollingQuestion].B = responseStats.B;
                        }
                        if (responseStats.C != null) {
                            self.pollingQuestionResponses[self.currentPollingQuestion].C = responseStats.C;
                        }
                        if (responseStats.D != null) {
                            self.pollingQuestionResponses[self.currentPollingQuestion].D = responseStats.D;
                        }
                        if (responseStats.correct_answer != null) {
                            self.pollingQuestionResponses[self.currentPollingQuestion].correct_answer = responseStats.correct_answer;
                        }
                        if (responseStats.num_responses != null) {
                            self.pollingQuestionResponses[self.currentPollingQuestion].num_responses = responseStats.num_responses;
                        }
                        self.pollingQuestionResponses[self.currentPollingQuestion].polled = true;
                        self.rebuildCurrentQuestion();
                    }
                });
            }
        };
        LiveViewController.prototype.rebuildCurrentQuestion = function () {
            var questionTextString = this.pollingQuestions[this.currentPollingQuestion].text;
            var aTextString = this.pollingQuestions[this.currentPollingQuestion].a_text;
            var bTextString = this.pollingQuestions[this.currentPollingQuestion].b_text;
            var cTextString = this.pollingQuestions[this.currentPollingQuestion].c_text;
            var dTextString = this.pollingQuestions[this.currentPollingQuestion].d_text;
            if (this.pollingQuestionResponses[this.currentPollingQuestion].polled) {
                questionTextString += " (Number of Responses: " + this.pollingQuestionResponses[this.currentPollingQuestion].num_responses + ")";
                aTextString += " (Response Rate: " + this.pollingQuestionResponses[this.currentPollingQuestion].A + "%)";
                bTextString += " (Response Rate: " + this.pollingQuestionResponses[this.currentPollingQuestion].B + "%)";
                cTextString += " (Response Rate: " + this.pollingQuestionResponses[this.currentPollingQuestion].C + "%)";
                dTextString += " (Response Rate: " + this.pollingQuestionResponses[this.currentPollingQuestion].D + "%)";
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "A") {
                $("#a-question-button").removeClass("btn-danger");
                $("#a-question-button").addClass("btn-success");
            }
            else {
                $("#a-question-button").removeClass("btn-success");
                $("#a-question-button").addClass("btn-danger");
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "B") {
                $("#b-question-button").removeClass("btn-danger");
                $("#b-question-button").addClass("btn-success");
            }
            else {
                $("#b-question-button").removeClass("btn-success");
                $("#b-question-button").addClass("btn-danger");
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "C") {
                $("#c-question-button").removeClass("btn-danger");
                $("#c-question-button").addClass("btn-success");
            }
            else {
                $("#c-question-button").removeClass("btn-success");
                $("#c-question-button").addClass("btn-danger");
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "D") {
                $("#d-question-button").removeClass("btn-danger");
                $("#d-question-button").addClass("btn-success");
            }
            else {
                $("#d-question-button").removeClass("btn-success");
                $("#d-question-button").addClass("btn-danger");
            }
            $('#question-text').text(questionTextString);
            $('#a-text').text(aTextString);
            $('#b-text').text(bTextString);
            $('#c-text').text(cTextString);
            $('#d-text').text(dTextString);
            $('#question-pagination').text("Polling Question: " + (this.currentPollingQuestion + 1) + "/" + this.pollingQuestions.length);
        };
        LiveViewController.prototype.pollQuestionsStudent = function (self) {
            this.$http.get("/live_lecture/curr_polling_question/get/" + this.liveLectureId)
                .success(function (response) {
                console.log(response);
                if (response == null || response == 'null') {
                    // no question
                    console.log("no question");
                    self.pollingQuestionStudent.question_id = 0;
                    self.pollingQuestionStudentExist = false;
                }
                else if (response.id != self.pollingQuestionStudent.question_id) {
                    // new question
                    console.log("new question");
                    self.pollingQuestionStudent.question_id = response.id;
                    self.pollingQuestionStudent.question_text = response.text;
                    self.pollingQuestionStudent.a_text = response.a_text;
                    self.pollingQuestionStudent.b_text = response.b_text;
                    self.pollingQuestionStudent.c_text = response.c_text;
                    self.pollingQuestionStudent.d_text = response.d_text;
                    self.pollingQuestionStudentExist = true;
                }
                self.$timeout(function () { self.pollQuestionsStudent(self); }, 5000);
            })
                .error(function (reponse) {
            });
        };
        LiveViewController.prototype.setStudentResponse = function (resp) {
            this.studentResponse = resp;
        };
        LiveViewController.prototype.studentQuestionReponse = function () {
            this.$http.get("/live_lecture/respond_to_question/" + this.userId + "/" + this.pollingQuestionStudent.question_id + "/" + this.studentResponse)
                .success(function (response) {
            })
                .error(function (response) {
            });
        };
        LiveViewController.prototype.endLiveLecture = function () {
            console.log("Ending live lecture...");
            var self = this;
            this.$http.get("/live_lecture/end/" + this.liveLectureId)
                .success(function (response) {
                if (response.results !== undefined && response.results == true) {
                    self.$window.location.href = '/';
                }
                else {
                    alert("Unable to end live lecture");
                }
            })
                .error(function (response) {
                alert("Unable to end live lecture");
            });
        };
        LiveViewController.$inject = ["$scope", "$http", "$timeout", "$window"];
        return LiveViewController;
    }());
    ClassMoodApp.LiveViewController = LiveViewController;
    ClassMoodApp.app.controller('LiveViewController', LiveViewController);
})(ClassMoodApp || (ClassMoodApp = {}));
