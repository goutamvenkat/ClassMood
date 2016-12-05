/// <reference path="../app.ts" />
/// <reference path="../../../../typings/bootbox/bootbox.d.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export class LectureListController {
        static $inject = ["$scope", "$http", "$window", "$routeParams"];
        public lectures:Array<LectureListModel>;
        public classId: number;
        public isStudent: boolean;
        private userId: number;
        constructor(private $scope: ng.IScope,
                    private $http: ng.IHttpService,
                    private $window: ng.IWindowService) {
                        this.$http = $http;
                        this.$scope = $scope;
                        this.$window = $window;
                        this.lectures = [];
                    }

        public init(classId: number): void {
            this.classId = classId;
            this.getCurrentlectures();
            this.getIsProfessor();
            this.getUserId();
        }

        private getCurrentlectures(): void {
            this.$http.get(`/get_lecture_list/${this.classId}`).success(
                (data: any, status) => {
                    this.lectures = data.results;
                }
            ).catch((error) => {
                console.log(error);
            });
        }

        private getUserId(): void {
            this.$http.get('/user_id').then(
                (response: any) => {
                    this.userId = response.results;
                }
            )
        }

        private getIsProfessor(): void {
            this.$http.get("/is_student").success(
                (is_student: any, status) => {
                    this.isStudent = is_student.results;
                }
            )
        }

        public addLecture(): void {
            bootbox.prompt({
                title: "Enter Lecture Name",
                value: 'Lecture Name',
                callback: (lectureName: string) => {
                    if (lectureName != null) {
                        if (this.isStudent !== true) {
                            this.$http.get(`/add_lecture/${this.classId}/${lectureName}`).then(
                                (response: any) => {
                                    console.log(response.data);
                                }
                            ).then(
                                () => {this.getCurrentlectures();}
                            )
                        }
                    } 
                }
            });
        }

        private setStudentLecture(lectureName: string): void {
            this.$http.get(`/set_student_lectures/${lectureName}/${this.userId}`).then(
                (response: any) => {
                    if (response.data === 'false') {
                        alert('Incorrect Class!');
                    } else {
                        this.getCurrentlectures();
                    }
                }
            )
        }

        private setProfLecture(lectureName: string): void {
            this.$http.get(`/createClass/${lectureName}`).then(
                (response: any) => {
                    if (response.data === 'false') {
                        alert('Incorrect Class!');
                    } else {
                        this.getCurrentlectures();
                    }
                }
            )
        }


        public goLive(lectId: number): void {
            this.$http.get(`/live_lecture/create/${lectId}`).then(
                (response: any) => {
                    if (response.data !== undefined) {
                        let classId = parseInt(response.data, 10);
                        this.$window.location.href = `/live_lecture/get/${classId}`;
                    }
                }
            )
        }

        public getPollingQuestions(lecture_id: number): void {
            if (this.isStudent !== true) {
                this.$window.location.href = `/pollingQuestionList/${this.classId}/${lecture_id}`;
            }
        }

        public deleteLecture(lecture_id: number): void {
            if (!this.isStudent) {
                this.$http.get(`/delete/lecture/${lecture_id}`).success(
                    (data: any, status) => {
                        if (data.results === true) {
                            this.getCurrentlectures();
                        }
                    }
                ).catch((error) => {
                    console.log(error);
                });
            }
        }
    }

    app.controller('LectureListController', LectureListController);
}