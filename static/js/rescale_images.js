// use on "load" instead of document.ready to wait for images to load 
$(window).on("load", function() {
    $('.image img').each(function() {
        var previewWidth = 320;
        var previewHeight = 180;
        var ratio = 0;

        var width = $(this).width();        
        var height = $(this).height();    
        ratio = width/previewWidth;

        $(this).css("width", previewWidth);
        $(this).css("height", height*ratio);

        var height = $(this).height();  

        if (previewHeight < height){
            $(this).css("height", previewHeight);
        }
        

    });
});