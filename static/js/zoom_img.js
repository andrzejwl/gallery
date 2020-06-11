$(window).on("load", function() {
    $('img').addClass('img-enlargable').click(function(){
        var src = $(this).attr('src');
        var modal;
        function removeModal(){ modal.remove(); $('body').off('keyup.modal-close'); }
        modal = $('<div>').css({
            background: 'RGBA(0,0,0,.5) url('+src+') no-repeat center',
            backgroundSize: 'contain',
            width:'80%', height:'80%',
            position:'fixed',
            zIndex:'10000',
            top: '100px', left:'100px',
            cursor: 'zoom-out'
        }).click(function(){
            removeModal();
        }).appendTo('body');
        //handling ESC
        $('body').on('keyup.modal-close', function(e){
          if(e.key==='Escape'){ removeModal(); } 
        });
    });
});