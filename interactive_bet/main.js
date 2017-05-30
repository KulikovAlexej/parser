APP = angular.module('App', ['ngRoute']);

APP.controller('Panel', function($scope, $http){
	$scope.webSite = {
		first: 'BetExplorer',
		second: 'Sports'
	}
	$scope.init = function(){
		$http({
			method: 'GET',
			url: 'http://localhost:5000/API/betExp.json'
		}).then(function(res){
			$scope.betExp = res.data.matches;
			return $http({
				method: 'GET',
				url: 'http://localhost:5000/API/sports.json'
			})
		}).then(function(res){
			$scope.sportsArr = res.data.matches;
			$scope.sortArray($scope.betExp);
			$scope.sortArray($scope.sportsArr);
			console.log($scope.betExp);
			$scope.sources = {
				first : $scope.betExp,
				second : $scope.sportsArr
			};
		});
		
	}
	
	$scope.selectedMatch = {
		first: null,
		second: null
	};
	$scope.firstMatch = null;
	$scope.secondMatch = null;
	$scope.oursMatches = [];
	$scope.match_day = new Date();
	$scope.leagues = ['РФПЛ', 'Английская Премьер-Лига', 'Серия А', 'Испанская Примера', 'Бундеслига', 'Лига чемпионов', 'Лига Европы'];
	$scope.sortArray = function(array){
		array.sort(function(a,b){
			if(a.league > b.league){
				return 1
			}
			if(a.league < b.league){
				return -1
			}
			else{
				if(a.owner > b.owner){
					return 1
				}
				if(a.owner > b.owner){
					return -1
				}
				else{return 0}
			}
	})
	}
	
	
	
	$scope.selectMatch = function(match){
		$scope.sources.first.forEach(function(match){
			match.active = false;
		});
		if(match != null) {
			
		}
		$scope.selectedMatch.first = match;
		match.active = true;
		// return $scope.firstMatch = match;
	}
	$scope.storeMatch = function(event, match){
		if(event.isDetails){
			return 
		}
		$scope.sources.second.forEach(function(match){
			match.active = false;
		});
		
		$scope.selectedMatch.second = match;
		// $scope.secondMatch = match;
		match.active = true;
		
		
		var similarMatches = {
			first: $scope.firstMatch,
			second: $scope.secondMatch
		};
		similarMatches = JSON.stringify(similarMatches);
		$scope.oursMatches.push(similarMatches);
		$http.post('API/storage.json' , similarMatches);
		$scope.deleteMatches();
		// console.info(similarMatches);
		// console.info($scope.sources.first.length);

	}
	$scope.deleteMatches = function(){
		if($scope.selectedMatch.first != null && $scope.selectedMatch.second != null){
			var index1 = $scope.sources.first.indexOf($scope.selectedMatch.first);
			var index2 = $scope.sources.second.indexOf($scope.selectedMatch.second);
			$scope.sources.first.splice(index1, 1);
			$scope.sources.second.splice(index2, 1);
			$scope.selectedMatch.first = $scope.selectedMatch.second = null;	
		}	
	}
	$scope.deleteOneMatch = function(match, source){
		if(source == $scope.sources.first){
			var index = source.indexOf(match);
			$scope.sources.first.splice(index, 1);
		}
		if(source == $scope.sources.second){
			var index = source.indexOf(match);
			console.log(index);
			$scope.sources.second.splice(index, 1);
		}
		// console.log(index);
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

	$scope.openMatch = function(event, match, source){
		event.isDetails = true;
		$scope[source] = match;
		console.log($scope[source])
	}
	
	console.log($scope.betExp);
	$scope.init();
})