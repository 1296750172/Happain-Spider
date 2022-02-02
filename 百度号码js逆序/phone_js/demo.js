const CryptoJS = require("crypto-js")

let times = Date.parse(new Date())

var text = `{"1":"1","3":"93ceac81a7650e33cdab3cee40d306528cf41efa","4":"24","5":"1536x864","6":"1536x824","7":",","8":"PDF%20Viewer,Chrome%20PDF%20Viewer,Chromium%20PDF%20Viewer,Microsoft%20Edge%20PDF%20Viewer,WebKit%20built-in%20PDF","9":"Portable%20Document%20Format,Portable%20Document%20Format","11":"1","12":"1","13":"true","14":"-480","15":"zh-CN","16":"","17":"1,1,1,1,1,0","18":"1.25","19":"8","20":"0","21":"","22":"Gecko,20030107,Google Inc.,,Mozilla,Netscape,Win32","23":"0,0,0","24":"1","25":"Google Inc. (Intel),ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.100.9805)","27":"Openwave/ UCWEB7.0.2.37/28/999","28":"false,false","29":"true,true,true","30":0,"31":8,"32":"46","34":"Win32","35":"false,true","41":true,"42":null,"43":null,"44":0.94,"60":false,"61":false,"62":false,"63":true,"64":false,"65":true,"69":0,"70":0,"71":"","72":"zh-CN,zh,en,zh-TW,en-US","78":"02f1d0f2acc57bd39851aa5efd7dc7736bd42295_81b0bb76dc542b994d9b39df205e23b7ff67fe7b0133be929862c6c8d0bff703","79":"0,0,0,0,0","80":"0,0,0,0,0","81":"0","82":"c8f40c61a933b83eb3e7fdd1d8a97e7d34adaa48","85":"c0b93953448db03b443377c181e7ae91fa3f4433","101":"a9fa3e2cc56cf8470db16df2f070085a58250b1d","103":${times},"106":2055,"107":"2.9.17","108":"https://haoma.baidu.com/appeal","109":"https://passport.baidu.com/","112":"","113":"","114":"1234","115":"","160":"","198":33,"199":"","200":"4"}`



function decode() {

    //ase加密
    let key = CryptoJS.enc.Utf8.parse('D4005D99405F446A'); //密钥必须是16位，且避免使用保留字符
    let iv = CryptoJS.enc.Utf8.parse('636014d173e04409'); //密钥必须是16位，且避免使用保留字符
    let encryptedData  = CryptoJS.AES.encrypt(text, key, {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        iv:iv
    });
    let hexData = encryptedData.ciphertext.toString();
    console.log(hexData);
    return hexData
}

decode()