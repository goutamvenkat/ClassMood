'use strict';

/* Controllers for Angular */
app.controller('professorClassListController', function($scope, $http, $log) {
	$http.get('/getProfessorClassList')
	.then(function successfulCallback(response) {
		//$scope.classList = response.data;
		$scope.classList = response.data.results;
	}, function errorCallBack(response) {
		$scope.classList = [];
	});
});

app.controller('createClass', function($scope) {

});