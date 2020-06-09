var hidden = true;

$(document).ready(function() {
    $("#form-toggler").on("click", function(e){
        if (hidden == true){
            $(".toggled").show();
            //showForm();
            hidden = false;
            $("#form-toggler").html("remove");
        } else{
            //hideForm();
            $(".toggled").hide();
            hidden = true;
            $("#form-toggler").html("add");
        }
    });
});


