'use strict';

var app = angular.module('ClassMoodApp');

/* Controllers for Angular */
app.controller("studentLectures", function($scope, $http) {
    // Get studentID from session token
    var studentID = 1;
    $http.get('/student_lectures/' + studentID)
        .then(function successfulCallback(response) {
            $scope.classList = response.data.results;
        }, function errorCallBack(response) {
            // Handle appropriately
        });    
});


app.controller('dialogController', function($scope, $log, $http) {
    $scope.openDialog = function() {
        document.getElementById('createclassname').parentNode.MaterialTextfield.change('');
        $scope.showError = false;
        dialog.showModal();
    };

    $scope.createClicked = function() {
        var error = true;
        // var className = document.getElementById('createclassname').value;
        var className = $scope.classname;
        var studentID = 1;
        console.log('Class name: ' + className);
        if (className !== '') {
            $http.post('/set_student_lectures/' + className + '/' + studentID)
            .then(function successfulCallback(response) {
                if (response.data === true) {
                    error = false;
                    document.querySelector('dialog').close();
                    document.location.reload();
                }
            }, function errorCallBack(response) {
                console.log("ERROR RESPONSE: " + response.data);
            });
        }
        $scope.showError = error;
    };

    $scope.cancelClicked = function() {
        var d = document.querySelector('dialog');
        d.close();
    };

    $scope.showError = false;
});