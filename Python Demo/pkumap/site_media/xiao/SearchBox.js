var tempItems;
xiao.SearchBox = function(divId) {
	// body...
	this.poiSearchForm = dojo.query("#" + divId + " #poiSearchForm")[0];
	this.routeSearchForm = dojo.query("#" + divId + " #routeSearchForm")[0];
	dojo.connect(this.poiSearchForm,'onsubmit', null, this.onQueryPoi);
	dojo.connect(this.routeSearchForm,'onsubmit', null, this.onQueryRoute);

	// register tab for search form
	/*jQuery(function() {
                jQuery("#tabs").tabs();
        });*/    
	
	xiao.Tabs("tabs");

	// register suggest box for poi search form and route search form
	jQuery("#keyword").autocomplete("/poi/auto/", {
		width: 320,
		max: 10,
		highlight: false,
		scroll: true,
		scrollHeight: 300,
		parse: function(data) {
			return jQuery.map(eval(data), function(row) {
				return {
					data: row,
					value: row,
					result: row 
				}
			});
		},
		formatItem: function(row, i, max) {
			return row;
		},
		formatResult: function(row) {
			return row[0].replace(/(<.+?>)/gi, '');
		}
	});

	jQuery("#startpt").autocomplete("/poi/auto/", {
		width: 320,
		max: 10,
		highlight: false,
		scroll: true,
		scrollHeight: 300,
		parse: function(data) {
			return jQuery.map(eval(data), function(row) {
				return {
					data: row,
					value: row,
					result: row 
				}
			});
		},
		formatItem: function(row, i, max) {
			return row;
		},
		formatResult: function(row) {
			return row[0].replace(/(<.+?>)/gi, '');
		}
	});
	jQuery("#endpt").autocomplete("/poi/auto/", {
		width: 320,
		max: 10,
		highlight: false,
		scroll: true,
		scrollHeight: 300,
		parse: function(data) {
			return jQuery.map(eval(data), function(row) {
				return {
					data: row,
					value: row,
					result: row 
				}
			});
		},
		formatItem: function(row, i, max) {
			return row;
		},
		formatResult: function(row) {
			return row[0].replace(/(<.+?>)/gi, '');
		}
	});
}

xiao.SearchBox.prototype.onQueryPoi = function (e) {
	e.preventDefault();	
	dataStore.fetch({
		type: "poi",
		keyword: this.keyword.value 
	},
	function(items){
		textInfoWindow.updatePoiInfo(items);
		mapInfoWindow.updatePoiInfo(items);
	}
	);
	return false;
}

xiao.SearchBox.prototype.onQueryRoute = function (e) {
	// body...
	e.preventDefault();
	
	// get coordinates of the two placenames
	var response1 = dataStore.fetch({
		type:"poi",
		keyword: this.startpt.value,
		sync:true
	});
	var startPois = response1.results[0];
	var response2 = dataStore.fetch({
		type:"poi",
		keyword:this.endpt.value,
		sync:true
	});
	var endPois = response2.results[0];	

	if (startPois.length === 1 && endPois.length ===1){
		if (startPois[0].footprint.indexOf("POINT") == 0 &&
			endPois[0].footprint.indexOf("POINT") == 0){
				dataStore.fetch({
					type:"route",
					keyword:{
						startCoord: startPois[0].footprint,
						endCoord: endPois[0].footprint
					}
				},
				function (routes) {
					// body...
					textInfoWindow.updateRouteInfo(routes);
					mapInfoWindow.updateRouteInfo(routes);
				}
				);
			}
	}
	else{
		//TODO: handle unclear placename conditions
	}
	
	return false;
}
