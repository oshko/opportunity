
deleteEntry = function(idName, aUrl) {
    var obsolete = $('#'+ idName + '-container input:checked')
    for (var i = 0; i < obsolete.length; i++) {
        $.ajax({
            url: aUrl + obsolete[i].value,
            dataType: 'json',
            success:  function (data) { 
                var selector = '#'+ data['idName'] + '-' + data['id']; 
                $(selector).remove() ;

                var n = $("#"+ data['idName'] +"-container ul div").length;
                if (n == 0) {
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
