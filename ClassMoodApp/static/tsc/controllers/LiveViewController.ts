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
        private userId: number;
        private lectureId: number;
        constructor(private $scope: ng.IScope,
                    private $http: ng.IHttpService,
                    private $timeout: ng.ITimeoutService) {
                        this.$http = $http;
                        this.$scope = $scope;
                        this.getIsStudent();
                        this.getUserId();
                        this.getLectureId();
                        this.gauge = new GaugeModel();
                        this.gauge.depth_num = 0;
                        this.gauge.pace_num = 0;
                        this.questionEntered = '';
						this.questions = new AnonymousQuestionsModel();
						this.questions.questions_array = [];
						this.questions.questions_string = '';
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
                    }
                    else
                    {
                        this.getGauge(this);
                    }
                }
            )
        }

        private getLectureId(): void {
            this.lectureId = parseInt($("#lectureId").attr('lecture-id'), 10);
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
            self.$http.get(`/live_lecture/gauge/get/${self.lectureId}`)
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
            this.$http.post('/live_lecture/gauge/update', JSON.stringify({lect_id: this.lectureId, pace_num: this.gauge.pace_num, depth_num: this.gauge.depth_num}))
            .success(function(data, status, headers, config) {
            })
            .error(function(data, status, header, config) {
                console.log("ERROR while posting current gauge");
            })
        }

        private gaugePollPace(self): void {
            this.$http.get(`/live_lecture/pace/get/${this.lectureId}`)
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
            this.$http.get(`/live_lecture/depth/get/${this.lectureId}`)
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
			this.$http.get(`/live_lecture/questions/get/${this.lectureId}`)
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
				this.$http.get(`/live_lecture/questions/put/${this.lectureId}/${this.questionEntered}`)
				.success(function (response: boolean) {
					self.questions.questions_array.push(self.questionEntered);
					self.questions.questions_string = self.questions.questions_array.join('\n');
					self.questionEntered = '';
				})
			}
		}
    }
    app.controller('LiveViewController', LiveViewController);
}