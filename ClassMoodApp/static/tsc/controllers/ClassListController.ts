/// <reference path="../app.ts" />
declare var angular: ng.IAngularStatic;
module ClassMoodApp {
    "use strict";
    export class ClassListController {
        static $inject = ["$scope", "$http", "$window"];
        public classes:Array<ClassListModel>;
        public isStudent: boolean;
        private userId: number;
        constructor(private $scope: ng.IScope,
                    private $http: ng.IHttpService,
                    private $window: ng.IWindowService) {
                        this.$http = $http;
                        this.$scope = $scope;
                        this.$window = $window;
                        this.classes = [];
                        this.getCurrentClasses();
                        this.getIsProfessor();
                        this.getUserId();
                    }

        private getCurrentClasses(): void {
            this.$http.get("/getClassList").success(
                (data: any, status) => {
                    this.classes = data.results;
                }
            ).catch((error) => {
                console.log(error);
            });
        }

        private getUserId(): void {
            this.$http.get('/user_id').then(
                (response: any) => {
                    this.userId = response.data.results;
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

        public addClass(): void {
            bootbox.prompt({
                title: "Enter Class Name",
                inputType: 'textarea',
                callback: (className: string) => {
                    if (className != null) {
                        if (this.isStudent === true) {
                            this.setStudentClass(className);
                        } else {
                            this.setProfClass(className);
                        }
                    } 
                }
            });
        }

        private setStudentClass(className: string): void {
            this.$http.get(`/set_student_classes/${className}/${this.userId}`).then(
                (response: any) => {
                    if (response.data === 'false') {
                        alert('Incorrect Class!');
                    } else {
                        this.getCurrentClasses();
                    }
                }
            )
        }

        private setProfClass(className: string): void {
            this.$http.get(`/createClass/${className}`).then(
                (response: any) => {
                    if (response.data === 'false') {
                        alert('Incorrect Class!');
                    } else {
                        this.getCurrentClasses();
                    }
                }
            )
        }

        public joinLecture(liveLectureId: number): void {
            if (this.isStudent === true) {
                this.$http.get(`/join_live_lecture/${liveLectureId}`).then(
                    (response: any) => {
                        console.log(`JOINED LECTURE AND UPDATED STUDENT COUNT: ${response.data}`);
                        if (response.data !== undefined) {
                            var classId = parseInt(response.data, 10);
                            if (classId > 0) {
                                // At this point just open the lecture page so that students and professor are both viewing the same material (Except for gauges).
                                this.$window.location.href = `/live_lecture/get/${classId}`;
                            } else {
                                alert("Invalid class id returned.");
                            }
                        }
                    }
                )
            }
        }

        public deleteClass(classId: number) {
            if (this.isStudent) {
                this.$http.get(`/delete/class_student/${this.userId}/${classId}`).success(
                    (data: any, status) => {
                        if (data.results === true) {
                            this.getCurrentClasses();
                        }
                    }
                ).catch((error) => {
                    console.log(error);
                });
            } else {
                this.$http.get(`/delete/class/${classId}`).success(
                    (data: any, status) => {
                        if (data.results === true) {
                            this.getCurrentClasses();
                        }
                    }
                ).catch((error) => {
                    console.log(error);
                });
            }
        }

        public getClassLectures(classId: number): void {
            if (this.isStudent !== true) {
                this.$window.location.href = `/lectureList/${classId}`;
            }
        }
    }
    app.controller('ClassListController', ClassListController);
}