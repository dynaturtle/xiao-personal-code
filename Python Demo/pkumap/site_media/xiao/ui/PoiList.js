dojo.provide("xiao.ui.PoiList");
 
dojo.require("dijit._Widget");
dojo.require("dojox.dtl._DomTemplated");
// All the following requires are all just so this works in a XD env!
dojo.require("dojo.cache");
 
dojo.declare("xiao.ui.PoiList",
    [dijit._Widget,dojox.dtl._DomTemplated],
    {
		features:[],
		templatePath: dojo.moduleUrl("xiao.ui","PoiList.html"),
		postMixInProperties: function(){
		}
    }
);
