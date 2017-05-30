APP = angular.module('App', ['ngRoute']);

APP.controller('Panel', function($scope){
	$scope.webSite = {
		first: 'BetExplorer',
		second: 'Sports'
	}
	$scope.selectedMatch = null;
	$scope.match_day = new Date();
	$scope.leagues = ['РФПЛ', 'Английская Премьер-Лига', 'Серия А', 'Испанская Примера', 'Бундеслига', 'Лига чемпионов', 'Лига Европы'];
	$scope.betExp = [
		{league: 'Бундеслига', owner: 'Shal\'ke-04', guest: 'Nurnberg', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Zenit', guest: 'CSKA', score: '2:2', date: '24.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Зенит', guest: 'Краснодар', score: '1:0', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Zenit', guest: 'CSKA', score: '2:2', date: '23.05.2017', time: '18:00'},
		{league: 'Бундеслига', owner: 'Shal\'ke-04', guest: 'Nurnberg', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Zenit', guest: 'CSKA', score: '2:2', date: '24.05.2017', time: '18:00'},
		{league: 'Бундеслига', owner: 'Shal\'ke-04', guest: 'Nurnberg', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'Премьер-Лига', owner: 'Манчестер Юнайтед', guest: 'Манчестер Сити', score: '2:2', date: '23.05.2017', time: '18:00'},
		{league: 'Серия А', owner: 'Милан', guest: 'Ювентус', score: '1:1', date: '25.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Спартак', guest: 'Локомотив', score: '2:2', date: '23.05.2017', time: '18:00'}
	];
	$scope.sportsArr = [
		{league: 'Бундеслига', owner: 'Shal\'ke-04', guest: 'Nurnberg', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Zenit', guest: 'CSKA', score: '2:2', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Зенит', guest: 'Краснодар', score: '1:0', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Zenit', guest: 'CSKA', score: '2:2', date: '23.05.2017', time: '18:00'},
		{league: 'Бундеслига', owner: 'Shal\'ke-04', guest: 'Nurnberg', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Zenit', guest: 'CSKA', score: '2:2', date: '23.05.2017', time: '18:00'},
		{league: 'Бундеслига', owner: 'Shal\'ke-04', guest: 'Nurnberg', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'Премьер-Лига', owner: 'Манчестер Юнайтед', guest: 'Манчестер Сити', score: '2:2', date: '23.05.2017', time: '18:00'},
		{league: 'Серия А', owner: 'Милан', guest: 'Ювентус', score: '1:1', date: '23.05.2017', time: '18:00'},
		{league: 'РФПЛ', owner: 'Спартак', guest: 'Локомотив', score: '2:2', date: '23.05.2017', time: '18:00'}
	];
	$scope.sources = {
		first : $scope.betExp,
		second : $scope.sportsArr
	};
	$scope.selectMatch = function(match){
		$scope.sources.first.forEach(function(match){
			match.class = 'disabled';
		});
		if(match != null) {
			
		}
		$scope.selectedMatch = match;
		match.class = 'active';
		console.log(match.league);

	}
	$scope.changeLeague = function(event) {
		console.log(event);
	}
	$scope.validateDate = function (date) {
		var day = date.getDate();
		var month = date.getMonth() + 1;
		var year = date.getFullYear();
		if(day < 10){
			day = "0" + day;
		}
		if(month < 9){
			month = "0" + month;
		}
		return day + '.' + month + '.' + year;
	}
	// $scope.validateDate($scope.match_day);

	$scope.translationOnPanel = function(){
		// var source = angular.element(querySelector('.left_list table tbody tr').length);
		// console.log(source);
		// var elem = angular.element(document.querySelector(".left_list thead tr td"));
		// console.log(elem.html());
	}
	$scope.translationOnPanel();

})