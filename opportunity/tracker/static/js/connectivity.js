
deleteOnlinePresence = function () {
    var obsolete = $('#presence-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        // if i sent a url without base_url will the server do the right thing?
        $.ajax({
            url: '/onlinePresence/del/' + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#presence-' + data['id']; 
                $(selector).remove() ;
                // if 
                var n = $("#presence-container ul div").length;
                if (n == 0) {
                    $("#presence-container ul").remove();
                    $("#presence-container").text("There are no links to references at this time.");
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                    alert(xhr.status);
                    alert(thrownError);
                } 
        });
    }
}


// This function searches for all checkboxes in story-container. 
// For each delete the coresponding story from the database. 
deletePars = function() {
    var obsolete = $('#story-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        // if i sent a url without base_url will the server do the right thing?
        $.ajax({
            url: '/par/del/' + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#story-' + data['id']; 
                $(selector).remove() ;
                // if 
                var n = $("#story-container ul div").length;
                if (n == 0) {
                    $("#story-container ul").remove();
                    $("#story-container").text("There are no links to PAR based stories at this time.");
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                    alert(xhr.status);
                    alert(thrownError);
                } 
        });
    }
}
