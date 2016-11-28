/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export class LiveViewController {
        static $inject = ["$scope", "$http", "$timeout"];
        public isStudent: boolean;
        public gauge: GaugeModel;
        public questions: AnonymousQuestionsModel;
        public questionEntered: string;
        public pollingQuestions:Array<PollingQuestionListModel>;
        public pollingQuestionResponses:Array<PollingQuestionResponseModel>;
        private userId: number;
        private lectureId: number;
        private liveLectureId: number;
        private currentPollingQuestion: number;
        private currentlyPresenting: boolean;
        constructor(private $scope: ng.IScope,
                    private $http: ng.IHttpService,
                    private $timeout: ng.ITimeoutService) {
                        this.$http = $http;
                        this.$scope = $scope;
                        this.gauge = new GaugeModel();
                        this.gauge.depth_num = 0;
                        this.gauge.pace_num = 0;
                        this.questionEntered = '';
						this.questions = new AnonymousQuestionsModel();
						this.questions.questions_array = [];
						this.questions.questions_string = '';
                        this.currentPollingQuestion = 0;
                        this.currentlyPresenting = false;
                    }

        public init(lecture_id: number, live_lecture_id: number): void {
            this.lectureId = lecture_id;
            this.liveLectureId = live_lecture_id;
            this.getIsStudent();
            this.getUserId();
        }

        private getUserId(): void {
            this.$http.get('/user_id').then(
                (response: any) => {
                    this.userId = response.data.results;
                }
            )
        }

        private getIsStudent(): void {
            this.$http.get("/is_student").success(
                (is_student: any, status) => {
                    this.isStudent = is_student.results;
                    if (!this.isStudent)
                    {
                        this.gaugePollPace(this);
                        this.gaugePollDepth(this);
                        this.pollAnonymousQuestions(this);
                        this.getPollingQuestions();
                    }
                    else
                    {
                        this.getGauge(this);
                    }
                }
            )
        }

        private votePace(newPace: number): void {
            this.gauge.pace_num = newPace;
            this.postCurrentGauge();
        }

        private voteDepth(newDepth: number): void {
            this.gauge.depth_num = newDepth;
            this.postCurrentGauge();
        }

        private getGauge(self): void {
            self.$http.get(`/live_lecture/gauge/get/${self.liveLectureId}`)
            .success(function(response: any) {
                self.gauge.pace_num = response.results[0];
                if (self.gauge.pace_num == -1)
                {
                    var pace = $("#pace1");
                    $("#pace1").prop('checked', true);
                    $("#pace1").parent().addClass('active');
                }
                else if (self.gauge.pace_num == 1)
                {
                    $("#pace3").prop('checked', true);
                    $("#pace3").parent().addClass('active');
                }
                else
                {
                    $("#pace2").prop('checked', true);
                    $("#pace2").parent().addClass('active');
                }
                self.gauge.depth_num = response.results[1];
                if (self.gauge.depth_num == -1)
                {
                    $("#depth1").prop('checked', true);
                    $("#depth1").parent().addClass('active');
                }
                else if (self.gauge.depth_num == 1)
                {
                    $("#depth3").prop('checked', true);
                    $("#depth3").parent().addClass('active');
                }
                else
                {
                    $("#depth2").prop('checked', true);
                    $("#depth2").parent().addClass('active');
                }
            })
            .error(function(response: any) {
            })
        }

        private postCurrentGauge(): void {
            this.$http.post('/live_lecture/gauge/update', JSON.stringify({lect_id: this.liveLectureId, pace_num: this.gauge.pace_num, depth_num: this.gauge.depth_num}))
            .success(function(data, status, headers, config) {
            })
            .error(function(data, status, header, config) {
                console.log("ERROR while posting current gauge");
            })
        }

        private gaugePollPace(self): void {
            this.$http.get(`/live_lecture/pace/get/${this.liveLectureId}`)
            .success(function(response: number) {
                self.gauge.pace_num = response;
                $('#paceSlider').get(0).MaterialSlider.change(self.gauge.pace_num);
                self.$timeout(function() {self.gaugePollPace(self)}, 5000);
            })
            .error(function(response: any) {
                self.$timeout(function() {self.gaugePollPace(self)}, 10000);
            })
        }

        private gaugePollDepth(self): void {
            this.$http.get(`/live_lecture/depth/get/${this.liveLectureId}`)
            .success(function(response: number) {
                self.gauge.depth_num = response;
                $('#depthSlider').get(0).MaterialSlider.change(self.gauge.depth_num);
                self.$timeout(function() {self.gaugePollDepth(self)}, 5000);
            })
            .error(function(response: any) {
                self.$timeout(function() {self.gaugePollDepth(self)}, 10000);
            })
        }

        private pollAnonymousQuestions(self): void {
			this.$http.get(`/live_lecture/questions/get/${this.liveLectureId}`)
			.success(function(response: any) {
				console.log(response);
				self.questions.questions_array = response.results;
				self.questions.questions_string = self.questions.questions_array.join('\n');
				self.$timeout(function() {self.pollAnonymousQuestions(self)}, 5000);
			})
			.error(function(response: any) {
				self.$timeout(function() {self.pollAnonymousQuestions(self)}, 10000);
			})
		}

		private submitPressed(): void {
			this.submitAnonymousQuestion(this);
		}

		private submitAnonymousQuestion(self): void {
			if (this.questionEntered !== '') {
				this.$http.get(`/live_lecture/questions/put/${this.liveLectureId}/${this.questionEntered}`)
				.success(function (response: boolean) {
					self.questions.questions_array.push(self.questionEntered);
					self.questions.questions_string = self.questions.questions_array.join('\n');
					self.questionEntered = '';
				})
			}
		}

        public resetGauges(): void {
            if (!this.isStudent) {
                this.$http.get(`/reset_gauges/${this.lectureId}`).success(
                    (data: any, status) => {
                        if (data.results === true) {
                            this.gaugePollPace(this);
                            this.gaugePollDepth(this);
                        }
                    }
                ).catch((error) => {
                    console.log(error);
                });
            }
        }

        private getPollingQuestions(): void {
            var self = this;
            this.$http.get(`/get_polling_questions/${this.lectureId}`)
            .success(function (response: any) {
                self.pollingQuestions = response.results;
                self.pollingQuestionResponses = [];
                if (self.pollingQuestions.length > 0) {
                    for (var i = 0; i < self.pollingQuestions.length; i++) {
                        var currentResponse = new PollingQuestionResponseModel();
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
            })
        }

        public previousPollingQuestion(): void {
            if (!this.currentlyPresenting) {
                this.currentPollingQuestion -= 1;
                if (this.currentPollingQuestion < 0) {
                    this.currentPollingQuestion = 0;
                } else {
                    this.rebuildCurrentQuestion();
                }
            }
        }

        public nextPollingQuestion(): void {
            if (!this.currentlyPresenting) {
                this.currentPollingQuestion += 1;
                if (this.currentPollingQuestion >= this.pollingQuestions.length) {
                    this.currentPollingQuestion = this.pollingQuestions.length - 1;
                } else {
                    this.rebuildCurrentQuestion();
                }
            }
        }

        public beginPresentingQuestion(): void {
            if (!this.currentlyPresenting) {
                var self = this;
                this.$http.get(`/live_lecture/present_polling_question/get/${this.liveLectureId}/${this.pollingQuestions[this.currentPollingQuestion].id}`)
                .success(function (response: any) {
                    self.currentlyPresenting = true;
                })
            }
        }

        public stopPresentingQuestion(): void {
            if (this.currentlyPresenting) {
                var self = this;
                this.$http.get(`/live_lecture/stop_polling_questions/${this.liveLectureId}`)
                .success(function (response: Array<PollingQuestionResponseModel>) {
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
                })
            }
        }

        private rebuildCurrentQuestion(): void {
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
            } else {
                $("#a-question-button").removeClass("btn-success");
                $("#a-question-button").addClass("btn-danger");
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "B") {
                $("#b-question-button").removeClass("btn-danger");
                $("#b-question-button").addClass("btn-success");
            } else {
                $("#b-question-button").removeClass("btn-success");
                $("#b-question-button").addClass("btn-danger");
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "C") {
                $("#c-question-button").removeClass("btn-danger");
                $("#c-question-button").addClass("btn-success");
            } else {
                $("#c-question-button").removeClass("btn-success");
                $("#c-question-button").addClass("btn-danger");
            }
            if (this.pollingQuestions[this.currentPollingQuestion].answer == "D") {
                $("#d-question-button").removeClass("btn-danger");
                $("#d-question-button").addClass("btn-success");
            } else {
                $("#d-question-button").removeClass("btn-success");
                $("#d-question-button").addClass("btn-danger");
            }

            $('#question-text').text(questionTextString);
            $('#a-text').text(aTextString);
            $('#b-text').text(bTextString);
            $('#c-text').text(cTextString);
            $('#d-text').text(dTextString);
            $('#question-pagination').text("Polling Question: " + (this.currentPollingQuestion + 1) + "/" + this.pollingQuestions.length);
        }
    }
    app.controller('LiveViewController', LiveViewController);
}