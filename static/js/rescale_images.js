// use on "load" instead of document.ready to wait for images to load 
$(window).on("load", function() {
    $('.image img').each(function() {
        $(this).css("width", previewWidth);
        $(this).css("height", previewHeight);
    });
});