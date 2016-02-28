var map;
var positive = new L.LayerGroup([]);
var	negative = new L.LayerGroup([]);

var drawMap = function() {
	L.mapbox.accessToken = 'pk.eyJ1IjoiZ25nY3AiLCJhIjoiY2lsNXd5b3ZrMDA0a3UybHoxY3h5NGN3eiJ9.OrXfMbZ123f3f1EfPRCHHA';
	var southWest = L.latLng(0, -170),
    northEast = L.latLng(60, 0),
    bounds = L.latLngBounds(southWest, northEast);

	map = L.mapbox.map('map', 'gngcp.p97o5d8j', {
		maxBounds: bounds,
		maxZoom: 20,
		minZoom: 3
	}).setView([40, -97], 5);

	var layer = L.mapbox.tileLayer('gngcp.p97o5d8j');
	layer.on('ready', function(){
		getData();
	});
}

var getData = function() {
	var source = new EventSource($SCRIPT_ROOT + "/tweets");
	source.onmessage = function(event) {
	    if (event.data != "1") {
	    	addLayers(JSON.parse(event.data));
		}
	};  
}

var addLayers = function(singleData) {
	    var circle = new L.circleMarker([singleData.coord[0], singleData.coord[1]]).bindPopup(singleData.text);
	    circle.setRadius('10');

	    circle.options.fillColor = '#870029';
	    circle.options.color = '#870029';

	     /* circle.options.fillColor = '#4CAF50';
	      circle.options.color = '#4CAF50'; */

	    //Builds layer groups 
	      positive.addLayer(circle);
	      // negative.addLayer(circle);

	    populateFeed(singleData);

	 positive.addTo(map);
	 negative.addTo(map);
}



var populateFeed = function(singleData) {
	var infoPiece = document.createElement("div");
	infoPiece.className = "infoPiece";

	var textData = document.createElement("p");
	infoPiece.appendChild(textData);

	var tokens = singleData.text.match(/\S+/g);
	for (i = 0; i < tokens.length; i++) {
		if (tokens[i].charAt(0) != '#') {
			if (tokens[i].substring(0, 8) != "https://") {
				textData.innerHTML += tokens[i] + " ";
			} else {
				textData.innerHTML += "<a href='" + tokens[i] + "'>" + tokens[i] + " </a>";
			}
		} else {
			textData.innerHTML += "<a href='https://twitter.com/hashtag/" + tokens[i].substring(1, tokens[i].length) + "'>" + tokens[i] + " </a>";
		}
	}

	$("#twitter").prepend(infoPiece);
}
