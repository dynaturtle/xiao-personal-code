xiao = {
	includedModules : {},
	path : "/site_media/"
};

xiao.include = function (moduleName) {
		// body...
		if (xiao.includedModules[moduleName])
				return;
		xiao.includedModules[moduleName] = true;
		relativePath = moduleName.replace(/\./g, '/') + ".js";
		modulePath = xiao.path + relativePath;
		content = dojo.xhrGet({
			url: modulePath,
			handleAs: 'javascript',
			sync: true
		});
		eval(content);
		head = document.getElementsByTagName("head")[0];
		script = document.createElement("script");
		script.setAttribute("type","text/javascript");
		script.setAttribute("src",modulePath);
		head.appendChild(script);
}
