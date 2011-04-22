xiao.TextInfoWindow = function(divId) {
	this.domNode = dojo.byId(divId);
}

xiao.TextInfoWindow.prototype.updatePoiInfo = function(features) {
	console.log("update following pois:", features[0]);
	if (this.domNode.firstChild)
		this.domNode.removeChild(this.domNode.firstChild);
	var node = document.createElement("div");
	this.domNode.appendChild(node);
	var poiList = new xiao.ui.PoiList({
		features: features 
	},node);
	console.log("pois update finish");
}

xiao.TextInfoWindow.prototype.updateRouteInfo = function(routes) {
	// body...
	console.log("update following routes:", routes);
	if (this.domNode.firstChild)
		this.domNode.removeChild(this.domNode.firstChild);
	var node = document.createElement("div");
	this.domNode.appendChild(node);
	var routeList = new xiao.ui.RouteList({
		routes: routes
	},node);
}
