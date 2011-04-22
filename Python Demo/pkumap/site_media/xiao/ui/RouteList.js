dojo.provide("xiao.ui.RouteList");
 
dojo.require("dijit._Widget");
dojo.require("dojox.dtl._DomTemplated");
// All the following requires are all just so this works in a XD env!
dojo.require("dojo.cache");
 
dojo.declare("xiao.ui.RouteList",
    [dijit._Widget,dojox.dtl._DomTemplated],
    {
		routes:[],
		templatePath: dojo.moduleUrl("xiao.ui","RouteList.html"),
		postMixInProperties: function(){
		}
    }
);
