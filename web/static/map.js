var map;
var choose = true;
var positive = new L.LayerGroup([]);
var	negative = new L.LayerGroup([]);
var NYT = "http://api.nytimes.com/svc/topstories/v1/national.json?api-key=b6467e1fd3401efb76c76c978f01f015:5:74562598";

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
	L.geoJson(statesData, {style: style}).addTo(map);
	layer.on('ready', function(){
		getData();
		getNews();
		$('#news').hide(); // Starts Hidden
	});
}

function getColor(d) {
	 return d > 80 ? '#15811a' :
           d > 60  ? '#319635' :
           d > 25  ? '#55b059' :
           d > 5  ? '#7ecc82' :
           d > -5   ? '#d3d3d3' :
           d > -25   ? '#d489a0' :
           d > -60   ? '#bd5776' :
           d > -80    ? '#9a1f44' :
					  '#870029' ;
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.score / feature.properties.count * 100),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.5
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
	var circle = new L.circleMarker([singleData.place.bounding_box.coordinates[0][0][1], singleData.place.bounding_box.coordinates[0][0][0]]).bindPopup(singleData.text);
    circle.setRadius('2');
    $(circle._icon).addClass('marker');
    if (choose) {
	    circle.options.fillColor = '#870029';
		circle.options.color = '#870029';
		choose = false;
	} else {
		circle.options.fillColor = '#4CAF50';
		circle.options.color = '#4CAF50';
		choose = true;
	}
    populateFeed(singleData);
	circle.addTo(map);
	for (i = 0; i < statesData.length; i++) {
		if (statesData[i].properties.abbr == singleData.place.full_name.split(',')[1]); {
			statesData[i].properties.count++;
			if (singleData.score == "positive") {
				statesData[i].properties.score += 1;
			} else {
				statesData[i].properties.score -= 1;
			}
			L.geoJson(statesData[i], {style: style}).addTo(map);
		}
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
		var link = document.createElement("a");
		link.href = dat[i].url;
		link.innerHTML = dat[i].url;
		infoPiece.appendChild(title);
		infoPiece.appendChild(author);
		infoPiece.appendChild(link);

		$("#news").prepend(infoPiece);
	}
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
