dojo.require("dijit.layout.LayoutContainer");
dojo.require("dijit.Toolbar");
dojo.require("dijit.layout.SplitContainer");
dojo.require("dijit.layout.AccordionContainer");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.form.Button");
dojo.require("dijit.form.TextBox");
dojo.require("dijit.TitlePane");
dojo.require("dojox.layout.ContentPane");
dojo.registerModulePath("xiao.ui", "../../../xiao/ui");
dojo.require("xiao.ui.PoiList");
xiao.include("xiao.MapInfoWindow");
xiao.include("xiao.TextInfoWindow");
xiao.include("xiao.SpatialDataStore");
xiao.include("xiao.SearchBox");
xiao.include("xiao.NaviInfoWindow");
xiao.include("xiao.Tabs");
xiao.include("xiao.ui.PoiList");
xiao.include("xiao.ui.RouteList");

//some patch for OpenLayers

// Patch for OpenLayers TMS is needed because string "1.0.0" is hardcoded in url no,
// there has to be optional parameter with version (default this "1.0.0")
// Hack to support local tiles by stable OpenLayers branch without a patch
OpenLayers.Layer.TMS.prototype.getURL = function(bounds){
    bounds = this.adjustBounds(bounds);
    var res = this.map.getResolution();
    var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
    var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));
    var z = this.map.getZoom();
    var path = z + "/" + x + "/" + y + "." + this.type;
    var url = this.url;
    if (url instanceof Array) {
        url = this.selectUrl(path, url);
    }
    return url + path;
};

jQuery.noConflict();
dojo.addOnLoad(init);


//globe
var mapInfoWindow;
var textInfoWindow;
var naviInfoWindow;
var dataStore;	
var searchBox;

function init () {
	mapInfoWindow = new xiao.MapInfoWindow("mainMap");
	textInfoWindow = new xiao.TextInfoWindow("textInfoWindow");
	naviInfoWindow = new xiao.NaviInfoWindow("naviInfoWindow");
	dataStore = new xiao.SpatialDataStore("/");
	searchBox = new xiao.SearchBox("mapsearch");
}
