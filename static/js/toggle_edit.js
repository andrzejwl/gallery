var formToggled = [];

function toggleEdit(id, action){
    var div = $('#desc-text'+id);
    var description = div.html();
    if (!formToggled.includes(id)){
        var form = `
            <form method="POST" action="`+action+`">
                <input type="text" value="`+description+`" name="new_desc">
                <input type="hidden" value=`+id+` name="image_id">
                <input type="submit" value="save">
            </form>`
        div.html(form);
        formToggled.push(id);
    }
}