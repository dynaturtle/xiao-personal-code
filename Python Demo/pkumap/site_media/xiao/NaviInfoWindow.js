xiao.NaviInfoWindow = function(divId) {
	this.domNode = dojo.byId(divId);
	dojo.query("a", this.domNode).onclick(function(e){
		console.log("context", this.innerHTML);
		dataStore.fetch({
			type: "poi",
			keyword: this.innerHTML
		},
		function(items){
			textInfoWindow.updatePoiInfo(items);
			mapInfoWindow.updatePoiInfo(items);
		}
		);
	});
}
