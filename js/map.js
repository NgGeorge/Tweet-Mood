var drawMap = function() {
	L.mapbox.accessToken = 'pk.eyJ1IjoiZ25nY3AiLCJhIjoiY2lsNXd5b3ZrMDA0a3UybHoxY3h5NGN3eiJ9.OrXfMbZ123f3f1EfPRCHHA';
	var map = L.mapbox.map('map', 'mapbox.streets').setView([40, -75], 9);
	var layer = L.mapbox.tileLayer('mapbox.streets');
	layer.on('ready', function(){

	});
}

var getData = function() {

}

var addLayers = function() {

}