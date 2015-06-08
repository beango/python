function Sharebtn(social,url,winWidth,winHeight) {
    var winTop = (screen.height / 2) - (winHeight / 2);
    var winLeft = (screen.width / 2) - (winWidth / 2);
    if (social == "facebook") {
        window.open('http://www.facebook.com/sharer.php?u='+encodeURIComponent(url)+'&display=popup', 'fbshare'+Math.random(), 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);   
    } else if (social == "google") {
        window.open('https://plus.google.com/share?url='+encodeURIComponent(url), 'gshare'+Math.random(), 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);     
    } else if (social == "twitter") {
        window.open('https://twitter.com/share', 'tshare'+Math.random(), 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    } else if (social == "weibo") {
        window.open('http://service.weibo.com/share/share.php?url='+encodeURIComponent(url), 'wshare'+Math.random(), 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    } else if (social == "linked") {
        window.open('https://www.linkedin.com/cws/share?url='+encodeURIComponent(url), 'lshare'+Math.random(), 'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);   
    }
    
}