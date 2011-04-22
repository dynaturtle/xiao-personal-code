xiao.SpatialDataStore = function (url) {
	// body...
	this.url = url;
}


/*
query:
the filter varible for gettting remote data
onItems:
callback of functions
return as following
onItems(items,ioArgs)
*/
xiao.SpatialDataStore.prototype.fetch = function (query, onItems) {
	// body...
	resource_url = this.url;
	queryContent = {};
	if (query.type){
		if (query.type ==='poi'){
			resource_url = this.url + 'poi/';
			queryContent.q = query.keyword;
		}	
		else if (query.type === 'building'){
			resource_url = this.url + 'poi/buidling/';
			queryContent.q = query.keyword;
		}
		else if (query.type == 'department'){
			resource_url = this.url + 'poi/department/';
			queryContent.q = query.keyword;
		}
		else if (query.type == 'scene' ){
			resource_url = this.url + 'poi/scene/';
			queryContent.q = query.keyword;
		}
		else if (query.type == 'route'){
			resource_url = this.url + 'route/coordinate/';
			queryContent.start = query.keyword.startCoord;
			queryContent.end = query.keyword.endCoord;
		}
		else throw "unrecongnized type";
	}
	
	if (query.sync)
		syncFlag = true;
	else 
		syncFlag = false;
		
	var res = dojo.xhrGet({
		url:resource_url,
		content:queryContent,
		handleAs:"json",
		load:onItems,
		sync: syncFlag
	});
	
	return res;
}
