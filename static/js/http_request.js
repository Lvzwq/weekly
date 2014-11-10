function HTTPRequest() {}
HTTPRequest.prototype.run = function() {
	if(this.request && this.request.readyState == 4 && this.state) {
		var status = this.request.status;
		this.state = 0;
		var request = this.request;
		this.request = null;
		if(status == 200) {
			if(this.onresponse) {this.onresponse(request);}
		}
		else if(this.onerror) this.onerror(request);
        else if(this.onerrer) this.onerrer(request);
	}
}
HTTPRequest.createXMLHTTP = function(){
	if(window.XMLHttpRequest) {return new XMLHttpRequest();}
	else if(window.ActiveXObject) {
		try {return new ActiveXObject("Microsoft.XMLHTTP");}
		catch(e) {return new ActiveXObject("Msxml2.XMLHTTP");}
	}
	else throw "您的浏览器不支持ajax。";
}
HTTPRequest.enabled = true;
try{HTTPRequest.createXMLHTTP();}
catch(e){HTTPRequest.enabled = false;}
HTTPRequest.prototype.getRequest = function() {
	this.request = HTTPRequest.createXMLHTTP();
	var _http = this;
	this.request.onreadystatechange = function(){_http.run();}
}
HTTPRequest.prototype.send = function(url, text, method) {
    if(this.onsend && this.onsend(url, text, method) == false) return;
	if(this.state == 1) {this.request.onreadystatechange = function(){};}
	try{this.getRequest();}
	catch(e){return;}
	this.state = 1;
	if(!method || method.toLowerCase() != "post") method = "get";
	if(!text) text = "";
	this.request.open(method, url ,true);
	if(method == "post") this.request.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	this.request.setRequestHeader("Request-Type","xml-http-request");
	this.request.send(text);
}
HTTPRequest.prototype.get = function(url) {
	this.send(url, "", "get");
	this.run();
}
HTTPRequest.prototype.onerror = function(request){
	if(confirm("连接服务器出错，错误码：" + request.status + "，是否查看错误信息？")){
	    var w = window.open("");
	    if(w){
	        w.document.write(request.responseText);
	        if(this.onshowerror) this.onshowerror(w.document.title);
	    }
	    else document.write(request.responseText);
	}
}