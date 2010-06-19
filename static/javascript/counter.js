var rid = 0;
var inc = true;
function onKeyDown(event)
{
    var id = $('.Selected').attr("id");
    if (inc &&  event.which == 32) {
	client_side_inc( id );
    }
    else {
	selectComponent(id);
    }
}
function cancelKeyDown()
{
   inc = false;
}

function enableKeyDown()
{
    inc = true;
}

function init() {
    enableKeyDown();
    $(document).keydown(onKeyDown);
    
    $("input").focus(cancelKeyDown);
    $("input").blur(enableKeyDown);

    selectComponent($('.Selected').attr("id"));
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

    $('.Selected').attr('class', "");
    $('#' + id).filter('[id='+id+']').attr('class', "Selected");

    $.ajax({type: 'GET',
		url: "/row",
		data: {'id' : id}, 
		success: updateCount});
}

function updateCount(count)
{
    $('.count').html(count);
}


function toggleModify(id) {
    button = $("#" + id + " .toggleModify");
    selectComponent(id);
    if (button.attr("value") == "Modify")
	{
	    $(".toggleModify").attr("value", "Modify");
	    button.attr("value", "Cancel");
	    $('.Component .update').hide();
	    
	    $('.Component .update').hide();
	    $('.Component .update').filter('[id='+id+']').show('fast');
	}
    else
	{
	    $(".toggleModify").attr("value", "Modify");
	    $('.Component .update').hide();
	}

}
