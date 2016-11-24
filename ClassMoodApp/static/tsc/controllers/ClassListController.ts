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

        public createLecture(): void {
            bootbox.prompt({
                title: "Enter Class Name",
                inputType: 'textarea',
                callback: (className: string) => {
                    if (className != null) {
                        console.log(className);
                        // go to the lecture list page
                    } 
                }
            });
        }

        // public addLecture(className:string): void {
        //     this.$http.get(`/add_lecture/${className}`).then(
        //         (response: any) => {
        //             console.log(`NEW LECTURE ID: ${response.data}`);
        //         }
        //     ).then(
        //         () => {this.getCurrentClasses();}
        //     )
        // }

        public joinLecture(liveLectureId: number): void {
            if (this.isStudent === true) {
                this.$http.get(`/join_lecture/${liveLectureId}`).then(
                    (response: any) => {
                        console.log(`JOINED LECTURE AND UPDATED STUDENT COUNT: ${response.data}`);
                    }
                )
            }
            // At this point just open the lecture page so that students and professor are both viewing the same material (Except for gauges).
            this.$window.location.href = `/live_lecture/get/${liveLectureId}`;
        }

        public getClassLectures(classId: number): void {
            if (this.isStudent !== true) {
                this.$window.location.href = `/lectureList/${classId}`;
            }
        }
    }
    app.controller('ClassListController', ClassListController);
}