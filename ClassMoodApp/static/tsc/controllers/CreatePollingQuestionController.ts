/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export class CreatePollingQuestionController {
        static $inject = ["$scope", "$http", "$window"];
        public questions:Array<CreatePollingQuestionModel>;
        public lecture_id: number;
        public isStudent: boolean;
        private userId: number;
        private classId: number;
        constructor(private $scope: ng.IScope,
                    private $http: ng.IHttpService,
                    private $window: ng.IWindowService) {
                        this.$http = $http;
                        this.$scope = $scope;
                        this.$window = $window;
                        let curLink = $window.location.pathname.split("/");
                        this.classId = parseInt(curLink[curLink.length-3]);
                        this.lecture_id = parseInt(curLink[curLink.length-2]);
                    }

        public submitPollingQuestion(): void {
		let text = this.question_text;
		let a = this.a_text;
		let b = this.b_text;
		let c = this.c_text;
		let d = this.d_text;
		let ans = this.ans;
		let options = [a, b, c, d];
		// Ignore option a because we check that it is not undefined later
		for (let i = 1; i < options.length; i++) {
			if (options[i] === undefined) {
				options[i] = "";
			}
		}
		console.log(text + " " + a + " " + b + " " + c + " " + d + " " + ans);
		if (!this.isStudent) {
			if (text && a && ans.length != 0) {
				this.$http.get(`/create_polling_question/${this.lecture_id}/${text}/${a}/${b}/${c}/${d}/${ans}`).then(
					(response: any) => {
						if (response.data) {
							this.$window.location.href = `/pollingQuestionList/${this.classId}/${this.lecture_id}`;
						}
				});
			} else {
				window.alert("Please enter a question and at least one answer choice.");
			}
		}
        }

    }
    app.controller('CreatePollingQuestionController', CreatePollingQuestionController);
}