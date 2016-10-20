'use strict';
var app = angular.module('ClassMoodApp');
/* Controllers for Angular */
app.controller('professorClassListController', function($scope, $http, $log) {
	$http.get('/getProfessorClassList')
	.then(function successfulCallback(response) {
		$scope.classList = response.data.results;
	}, function errorCallBack(response) {
		$scope.classList = [];
	});
});

app.controller('dialogProfessorController', function($scope, $log, $http) {
	$scope.openDialog = function() {
		document.getElementById('createclassname').parentNode.MaterialTextfield.change('');
		$scope.showError = false;
		var d = document.querySelector('dialog');
		dialog.showModal();
	};

	$scope.createClicked = function() {
		var error = true;
		var className = document.getElementById('createclassname').value;
		if (className !== '') {
			$http.post('/createClass/' + className)
			.then(function successfulCallback(response) {
				if (response.data == 'true') {
                    //successfully created the class
					error = false;
					var d = document.querySelector('dialog');
					d.close();
					document.location.reload();
				}
			}, function errorCallBack(response) {
			});
		}
		if (error) {
			$scope.showError = true;
		} else {
            document.location.refresh();
        }
	};

	$scope.cancelClicked = function() {
		var d = document.querySelector('dialog');
		d.close();
	};

	$scope.showError = false;
});


app.controller("studentClassListController", function($scope, $http) {
    // Get studentID from session token

    $http.get('/getAuth')
        .then(function successfulCallback(response) {
            var loggedIn = response.data.results
            // if (!loggedIn.id) TODO: throw error
            // if (!loggedIn) TODO: redirect to login page
            if (loggedIn.can_list_classes) var studentID = loggedIn.id;
            //probably should redirect to "access denied" page otherwise
            $http.get('/student_classes/' + studentID)
                .then(function successfulCallback(response) {
                    $scope.classList = response.data.results;
                }, function errorCallBack(response) {
                    // Handle appropriately
                });    
        }, function errorCallBack(response) {
            //TODO: implement
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
        if (className !== '') {
            $http.post('/set_student_classes/' + className + '/' + studentID)
            .then(function successfulCallback(response) {
                if (response.data == 'true') {
                    error = false;
                    document.querySelector('dialog').close();
                    document.location.reload();
                }
            }, function errorCallBack(response) {
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
