xiao.MapInfoWindow = function(divId){
	this.initMap(divId);
	this.initPoiLayer();
	this.initPathLayer();
}

xiao.MapInfoWindow.prototype.initMap = function(divId){
	//constant
	DEFAULT_LON = 495957.6415;
	DEFAULT_LAT = 313956.0701;
	DEFAULT_ZOOMLEVEL = 2;
	mapOptions = {
        maxExtent: new OpenLayers.Bounds(495304, 313061, 497008, 314765),
        maxResolution: 2.7264,
        numZoomLevels: 5,
        units: 'm',
        projection: "EPSG:2416",
        controls: [
			new OpenLayers.Control.PanZoomBar(), 
			new OpenLayers.Control.MouseDefaults(),
			new OpenLayers.Control.MousePosition()
		],
        eventListeners: {
            "moveend": function(){},
            "zoomend": function(){}
        }
    };
	
	this.map = new OpenLayers.Map(divId, mapOptions);
	
	//TODO: migrate baselayer data from 17.119 to host(224.111)
	var serverURL = 'http://162.105.17.119/';
	baseLayer = new OpenLayers.Layer.TMS("北京大学底图", serverURL + "data/tiles/background/", {
        layername: 'map',
        type: 'png'
    });

	this.map.addLayers([baseLayer]);
	this.map.setCenter(new OpenLayers.LonLat(DEFAULT_LON,DEFAULT_LAT));
    this.map.zoomTo(DEFAULT_ZOOMLEVEL);
}

xiao.MapInfoWindow.prototype.initPoiLayer = function() {
	var SHADOW_Z_INDEX = 1000;
	var MARKER_Z_INDEX = 1001;
	var poiLayerStyle = {
        styleMap: new OpenLayers.StyleMap({
            // Set the external graphic and background graphic images.
            externalGraphic: "/site_media/img/cuteMarker.png",
            backgroundGraphic: "/site_media/img/cuteMarkerShadow.png",

            // Makes sure the background graphic is placed correctly relative
            // to the external graphic.
            backgroundXOffset: -2,
            backgroundYOffset: -12,

            // Set the z-indexes of both graphics to make sure the background
            // graphics stay in the background (shadows on top of markers looks
            // odd; let's not do that).
            graphicZIndex: MARKER_Z_INDEX,
            backgroundGraphicZIndex: SHADOW_Z_INDEX,

            pointRadius: 10
        }),
        isBaseLayer: false,
        rendererOptions: {
            yOrdering: true
        }
    };
	this.poiLayer = new OpenLayers.Layer.Vector("poi layer", poiLayerStyle);
	this.map.addLayers([this.poiLayer]);
}

xiao.MapInfoWindow.prototype.initPathLayer = function() {
	// body...
	var pathLayerStyle = {
        styleMap: new OpenLayers.StyleMap({
			strokeColor: '#8070aa',
			strokeWidth: 4
        }),
        isBaseLayer: false
    };
	this.pathLayer = new OpenLayers.Layer.Vector("path layer", pathLayerStyle);
	this.map.addLayers([this.pathLayer]);
}

xiao.MapInfoWindow.prototype.updatePoiInfo = function(pois){
	this.poiLayer.destroyFeatures();
	var wktParser = new OpenLayers.Format.WKT();   	
    for (var i = 0; i < pois.length; i++) {
        var poi = pois[i];
		var featureArray = [];
		var feature = wktParser.read(poi.footprint);     
		var size = new OpenLayers.Size(21, 25);
		var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
		var icon = new OpenLayers.Icon("/site_media/img/marker.png", size, offset);
		
		//feature.data.icon = icon;
		feature.closeBox = true;
		feature.popupClass = OpenLayers.Popup;    
		feature.name = poi.name;
		feature.attributes = poi.attributes;
		feature.lonlat = feature.geometry.getBounds().getCenterLonLat();				
				
		//feature.data.popupContentHTML = PopupUI(feature.id + "ppc", feature); 
		featureArray.push(feature);
		this.poiLayer.addFeatures(featureArray);
    }

	//TODO: what if orgLayer has no feature
	if (pois.length != 0){
		var bounds = this.poiLayer.getDataExtent();
		// zoom to the best level
		if (bounds !== null){
			this.map.zoomToExtent(bounds);			
		}
	}
}

xiao.MapInfoWindow.prototype.updateRouteInfo = function(routes) {
	// body...
	this.pathLayer.destroyFeatures();
	var wktParser = new OpenLayers.Format.WKT();   
	for (var i = 0; i < routes.length; i++){
		var route = routes[i];
		var featureArray = [];
		var feature = wktParser.read(route.path);     
	        featureArray.push(feature);
		this.pathLayer.addFeatures(featureArray);
	}
	
	if (routes.length != 0){
		var bounds = this.pathLayer.getDataExtent();
		// zoom to the best level
		if (bounds !== null){
			this.map.zoomToExtent(bounds);			
		}	
	}
}
