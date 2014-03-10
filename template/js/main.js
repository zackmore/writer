(function(){
    // img click to open new page
    imgs = document.querySelectorAll('#article img');
    for(var i=0;i<imgs.length;i++){
        imgs[i].style.cursor = 'pointer';
        imgs[i].addEventListener('click', function(e){
            var elem = e.srcElement || e.target;
            window.open(elem.src);
        });
    }
})();
