/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    //Controller for polling question creation
    export class CreatePollingQuestionController {
        static $inject = ["$scope", "$http", "$window"];
        public questions:Array<CreatePollingQuestionModel>;
        public lecture_id: number;
        public isStudent: boolean;
        private userId: number;
        private classId: number;
        public question_text: string = '';
        public a_text: string = '';
        public b_text: string = '';
        public c_text: string = '';
        public d_text: string = '';
        public ans: string = 'A';
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
        //Submit a polling question (professor only)
        public submitPollingQuestion(): void {
			let text = encodeURIComponent(this.question_text);
			let a = encodeURIComponent(this.a_text);
			let b = encodeURIComponent(this.b_text);
			let c = encodeURIComponent(this.c_text);
			let d = encodeURIComponent(this.d_text);
			let ans = encodeURIComponent(this.ans);
			let url = `/create_polling_question/${this.lecture_id}/${text}/${a}/${b}/${c}/${d}/${this.ans}`;
			console.log(text + " " + a + " " + b + " " + c + " " + d + " " + this.ans);
			if (!this.isStudent) {
				if (text && ans.length != 0) {
					this.$http.get(url).then(
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