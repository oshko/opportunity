
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

/*

 * A section in the dashboard manages positions of interest for this
 * job search. They are separated into active and inactive. This
 * function toggles between the two. 

 * aRestUrl - is used to update the database. /position/{active|inactive}/{id}

 */

  toggleActiveStatus = function (aRestUrl) {

    $.ajax({
          url: aRestUrl,
	  dataType: 'json',
	  success:  function (data) { 
	  var source_tag = 'unk';
	  var new_id = 'unk';
	  var dest_tag = "unk";
	    
	  if (data['divId'] == 'position-inactive-container') {
	    // move from active to inactive list
	    source_tag = '#position-active-' + data['id'];
	    dest_tag = '#position-inactive-ul';
        dest_el = $(dest_tag)
        
        if(dest_el && dest_el.length==0) {
            // The inactive tab just contains a msg telling
            // the user it is empty. Replace the text with a list.
            
            // remove text message
            $('#position-inactive-container').text("");
            $('#position-inactive-container').append('<ul id="position-inactive-ul"></ul>');
            dest_el = $(dest_tag)
        }
	    $(source_tag).appendTo(dest_tag);

	    // update href 
	    tag = $(source_tag + " li a:first");
	    tag.text("active");
	    tag.attr("href", "javascript:toggleActiveStatus(\"/position/active/" + data['id']+ "\")");

	    // update id
	    $(source_tag).attr("id", "position-inactive-"+ data['id']);
	  } else {
	    // move from inactive to active list 
	    source_tag = '#position-inactive-' + data['id'];
	    dest_tag = '#position-active-ul';
        dest_el = $(dest_tag)
        
        if(dest_el && dest_el.length==0) {
            // The active tab just contains a msg telling
            // the user it is empty. Replace the text with a list.
            
            // remove text message
            $('#position-active-container').text("");
            $('#position-active-container').append('<ul id="position-active-ul"></ul>');
            dest_el = $(dest_tag)
        }
	    $(source_tag).appendTo(dest_tag);

	    // update href 
	    tag = $(source_tag + " li a:first");
	    tag.text("inactive");
	    tag.attr("href", "javascript:toggleActiveStatus(\"/position/inactive/" + data['id']+ "\")");

	    // update id
	    $(source_tag).attr("id", "position-active-"+ data['id']);
	  }
	      
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
