(function(){
    imgs = document.querySelectorAll('#article img');
    for(var i=0;i<imgs.length;i++){
        imgs[i].style.cursor = 'pointer';
        imgs[i].addEventListener('click', function(e){
            window.open(e.srcElement.src);
        });
    }
})();
