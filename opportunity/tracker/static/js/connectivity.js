
// This function searches for all checkboxes in story-container. 
// For each delete the coresponding story from the database. 
deletePars = function() {
    var obsolete = $('#story-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        // if i sent a url without base_url will the server do the right thing?
        $.get('/par/del/' + obsolete[i].value,
            function(data) {
                $('.story-' + data['id']).remove() ;
            }
        );
    }
}
