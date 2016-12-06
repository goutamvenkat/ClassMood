/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    //Controller for polling question lists
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

        //Get polling questions for current session
        private getPollingQuestions(): void {
            this.$http.get(`/get_polling_questions/${this.lecture_id}`).success(
                (data: any, status) => {
                    this.questions = data.results;
                }
            ).catch((error) => {
                console.log(error);
            });
        }

        //Start or join live session for a lecture
        public goLive(): void {
            this.$http.get(`/live_lecture/create/${this.lecture_id}`).then(
                (response: any) => {
                    let liveId = response.data;
                    this.$window.location.href = `/live_lecture/get/${this.classId}`;
                }
            )
        }

        //Bring up the UI to create a polling question
        public loadAddPollingQuestionsPage(): void {
            if (!this.isStudent) {
                this.$window.location.href = `/pollingQuestionList/${this.classId}/${this.lecture_id}/createPollingQuestion`;
            }
        }

        //Delete selected polling question
        public deletePollingQuestion(id: number): void {
            if (!this.isStudent) {
                this.$http.get(`/delete/polling_question/${id}`).success(
                    (data: any, status) => {
                        if (data.results === true) {
                            this.getPollingQuestions();
                        }
                    }
                ).catch((error) => {
                    console.log(error);
                });
            }
        }
    }

    app.controller('PollingQuestionListController', PollingQuestionListController);
}