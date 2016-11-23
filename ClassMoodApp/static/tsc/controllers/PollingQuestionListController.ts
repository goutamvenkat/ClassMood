/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export class PollingQuestionListController {
        static $inject = ["$scope", "$http", "$window"];
        public questions:Array<PollingQuestionListModel>;
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
                        this.classId = parseInt(curLink[curLink.length-2]);
                        this.lecture_id = parseInt(curLink[curLink.length-1]);
                        this.getPollingQuestions();
                    }

        private getPollingQuestions(): void {
            this.$http.get(`/get_polling_questions/${this.lecture_id}`).success(
                (data: any, status) => {
                    this.questions = data.results;
                }
            ).catch((error) => {
                console.log(error);
            });
        }

        public goLive(): void {
            this.$http.get(`/live_lecture/create/${this.lecture_id}`).then(
                (response: any) => {
                    let liveId = response.data;
                    this.$window.location.href = `/live_lecture/get/${this.classId}`;
                }
            )
        }

        public loadAddPollingQuestionsPage(): void {
            if (!this.isStudent) {
                this.$window.location.href = `/pollingQuestionList/${this.classId}/${this.lecture_id}/createPollingQuestion`;
            }
        }
    }

    app.controller('PollingQuestionListController', PollingQuestionListController);
}