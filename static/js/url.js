// JScript 文件

function GetUrl(ProtoString){
    var paraString =  ProtoString.split('#');
    if(!paraString[1]){
        return null;
    }
    var paras = paraString[1].split('&');
    var allParas=new Array(paras.length);
    for(var i = 0;i<paras.length; i++){
           allParas[GetPara(paras[i])[0]] = GetPara(paras[i])[1];
    }
    return allParas;
}

function GetPara(word){
    if(!word){
        return null;
    }
    var onePara = word.split('=');
    return onePara;
}