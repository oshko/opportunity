
deleteOnlinePresence = function () {
    var obsolete = $('#presence-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        $.ajax({
            url: '/onlinePresence/del/' + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#presence-' + data['id']; 
                $(selector).remove() ;
                
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

deletePitch = function() {
    var obsolete = $('#pitch-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        $.ajax({
            url: '/pitch/del/' + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#pitch-' + data['id']; 
                $(selector).remove() ;
        
                var n = $("#pitch-container ul div").length;
                if (n == 0) {
                    $("#pitch-container ul").remove();
                    $("#pitch-container").text("No elevator pitch.");
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
        $.ajax({
            url: '/par/del/' + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#story-' + data['id']; 
                $(selector).remove() ;

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
