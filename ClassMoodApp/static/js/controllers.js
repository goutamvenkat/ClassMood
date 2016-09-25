'use strict';

/* Controllers for Angular */
app.controller('professorClassListController', function($scope, $http, $log) {
	$http.get('/getProfessorClassList')
	.then(function successfulCallback(response) {
		$scope.classList = response.data.results;
	}, function errorCallBack(response) {
		$scope.classList = [];
	});
});

app.controller('dialogController', function($scope, $log, $http) {
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
				if (response.data === 'True') {
					error = false;
					var d = document.querySelector('dialog');
					d.close();
				}
			}, function errorCallBack(response) {
			});
		}
		if (error) {
			$scope.showError = true;
		}
	};

	$scope.cancelClicked = function() {
		var d = document.querySelector('dialog');
		d.close();
	};

	$scope.showError = false;
});
