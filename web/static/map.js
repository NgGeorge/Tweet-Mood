var currentState = "AL";
var stateLayers = new L.LayerGroup([]);
var map;
var NYT = "http://api.nytimes.com/svc/topstories/v1/national.json?api-key=b6467e1fd3401efb76c76c978f01f015:5:74562598";
var timer = null;
var filterManager = 0;
var layersOn = false;

var drawMap = function() {
	L.mapbox.accessToken = 'pk.eyJ1IjoiZ25nY3AiLCJhIjoiY2lsNXd5b3ZrMDA0a3UybHoxY3h5NGN3eiJ9.OrXfMbZ123f3f1EfPRCHHA';
	var southWest = L.latLng(0, -170),
    northEast = L.latLng(75, 0),
    bounds = L.latLngBounds(southWest, northEast);
	map = L.mapbox.map('map', 'gngcp.p97o5d8j', {
		maxBounds: bounds,
		maxZoom: 20,
		minZoom: 3
	}).setView([40, -97], 5);
	var layer = L.mapbox.tileLayer('gngcp.p97o5d8j');
	layer.on('ready', function(){
		getData();
		getNews();
		$('#news').hide(); // Starts Hidden
	});
	stateLayers.fillOpacity = .7;
}


function getColor(d) {
	 return d > 80 ? '#15811a' :
           d > 60  ? '#319635' :
           d > 30  ? '#55b059' :
           d > 15  ? '#7ecc82' :
           d > -15 ? '#d489a0' :
           d > -30 ? '#bd5776' :
           d > -60 ? '#9a1f44' :
		   d > -80 ? '#870029' :
		   			 '#d3d3d3' ;
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.score / feature.properties.count * 100),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.3
    };
}

var getData = function() {
	var source = new EventSource($SCRIPT_ROOT + "/tweets");
	source.onmessage = function(event) {
	    if (event.data != "1") {
	    	addLayers(JSON.parse(event.data));
		}
	};  
}

var getNews = function() {
	$.ajax({
	    url:NYT,
	    type: "get",
	    success:function(dat) {
	      data = dat;
	      buildNews(dat.results);
	    },
	    dataType: "json"
  	})
}

var addLayers = function(singleData) {
	currentState = singleData.place.full_name.split(',')[1].trim();
	if (currentState.length == 2) {
		var circle = new L.circleMarker([singleData.place.bounding_box.coordinates[0][0][1], singleData.place.bounding_box.coordinates[0][0][0]]).bindPopup(singleData.text);
	    circle.setRadius('5');
	    if (singleData.score == 'positive') {
		    circle.options.fillColor = '#4CAF50';
			circle.options.color = '#4CAF50';
		} else {
			circle.options.fillColor = '#870029';
			circle.options.color = '#870029';
		}
	    populateFeed(singleData);
		circle.addTo(map);
		for (i = 0; i < statesData.features.length; i++) {
			if (statesData.features[i].properties.abbr == currentState) {
					statesData.features[i].properties.count += 1;
				if (singleData.score == "positive") {
					statesData.features[i].properties.score += 1;
				} else {
					statesData.features[i].properties.score -= 1;
				}
				break;

			}
		}
	}
}

var toggleLayer = function() {

	if (!layersOn ) {
		L.geoJson(statesData, {style: style}).addTo(stateLayers);
		stateLayers.addTo(map);
		layersOn = true;
	} else {
		stateLayers.clearLayers();
		layersOn = false;
	}
}


var buildNews = function(dat){
	for (i = 0; i < dat.length; i++) {
		var infoPiece = document.createElement("div");
		infoPiece.className = "infoPiece";

		var title = document.createElement("p");
		title.innerHTML = dat[i].title;
		title.style.fontSize = "16pt";
		var author = document.createElement("p");
		author.innerHTML = dat[i].byline;
		author.className = "authors";
		var time = document.createElement("p");
		time.innerHTML = dat[i].published_date;
		var link = document.createElement("a");
		link.href = dat[i].url;
		link.innerHTML = dat[i].url;
		infoPiece.appendChild(title);
		infoPiece.appendChild(author);
		infoPiece.appendChild(time);
		infoPiece.appendChild(link);

		$("#news").prepend(infoPiece);
	}
}

var populateFeed = function(singleData) {
	if (filterManager == 10) {
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
		if (singleData.score == "positive") {
			infoPiece.style.borderLeft = "green solid 5px";
		} else {
			infoPiece.style.borderLeft = "#870029 solid 5px";
	    }
		$("#twitter").prepend(infoPiece); 
		filterManager = 0;
	} else {
		filterManager++;
	}
}
