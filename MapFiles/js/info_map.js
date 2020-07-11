//Map obj
var myMap = L.map("mapHere", {
    center: [39.8283, -98.5795],
    zoom: 4
});

// Adding tile layer to the map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox/dark-v10",
  accessToken: API_KEY
}).addTo(myMap);

var url = 'MapFiles/StateData.json';

d3.json(url, function(response) {
    console.log(response);
    //this is that cool lil pop up
    var clusters = L.markerClusterGroup();

    for(var i = 0; i < response.length; i++) {
        //location gets the location
        console.log(response[i].State)
        //trying to prevent myself from breaking my keyboard by redundancy 
        const { State, Order_type, Date, Status, NumTested, PerPositive, Lat, Lng} = response[i];

        if(State) {
            
            clusters.addLayer(L.marker([response[i].Lat, response[i].Lng]).bindPopup(
                    `Order Type: ${Order_type}
                    <br>Effective Date: ${Date}
                    <br>Order Status: ${Status}
                    <br># Tested: ${NumTested}
                    <br>% Positive: ${PerPositive}`
            )
                    
            )}
    }
    myMap.addLayer(clusters);
});

