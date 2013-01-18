
/*
 * This function is attached to a button. Deletes elements which have checked 
 * checkboxes in a div with a css id based on idName.
 */

deleteCheckedEntries = function(idName, aUrl) {
    var obsolete = $('#'+ idName + '-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        $.ajax({
            url: aUrl + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#'+ data['idName'] + '-' + data['id']; 
                $(selector).remove() ;

                if ($("#"+ data['idName'] +"-container ul div").length == 0) {
                    $("#" + data['idName'] + "-container ul").remove();
                    $("#" + data['idName'] + "-container").text(data['noElements']);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                    alert(xhr.status);
                    alert(thrownError);
                } 
        });
    }    
}

/*
 * DeleteEntry is attached to a link which is associated with a specific
 * object. This function calls the server delete the object from the database.
 * Then it removes the div section associated with it. 
 *  
 *  aRestUrl - a rest call to the server (e.g., "/interview/edit/1/activity")
 */

deleteEntry = function (aRestUrl) {
   $.ajax({
        url: aRestUrl,
        dataType: 'json',
        success:  function (data) { 
            var selector = '#'+ data['divId'] + '-' + data['id']; 
            $(selector).remove() ;

            if ($("#"+ data['divId'] +"-container ul div").length == 0) {
                $("#" + data['divId'] + "-container ul").remove();
                $("#" + data['divId'] + "-container").text(data['noElements']);
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        } 
    }); 
}
