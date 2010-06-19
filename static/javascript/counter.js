var rid = 0;

function init() {
    $(document).keydown(function(event) {

	    if (            event.which == 32) {
		event.preventDefault();
		

		var id = $('.ComponentSelected').attr("id");
		client_side_inc( id );
	    }
	});
    
    
    var id = $('.ComponentSelected').attr("id");

    selectComponent(id);
}

$(document).ready(init());

function client_side_inc( id )
{     
    rowCount = parseInt( $(".count").html() );
    rid += 1;
    
    $(".count").html(rowCount + 1);
    
    $.ajax(
	   {
	       type: "POST",
		   url: "/actions/IncrementRow.do",
		   data: {"id": id, "rid" : rid},
		   success: onIncrement
		   });
}

function onIncrement( resp )
{
    resp = JSON.parse(resp);

    crid = rid;
    nrid = parseInt(resp['rid']);
    id = resp['id'];

    if (nrid == crid)
	{
	    $(".count").html(resp['row']);
	}
}


function selectComponent(id)
{

    $('.ComponentSelected').attr('class', "ComponentDescription");
    $('#' + id).filter('[id='+id+']').attr('class', "ComponentSelected");

    $.ajax({type: 'GET',
		url: "/row",
		data: {'id' : id}, 
		success: updateCount});
}

function updateCount(count)
{
    $('.count').html(count);
}
