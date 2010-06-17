google.load("jquery", "1.4.2");

var rid = 0;

function onKeyDown( evt , id )
{
    var keynum = (window.event)?evt.keyCode:evt.which;

    if (keynum==32) {
	rowCount = parseInt( $("div#" + id + " .count").html() );
	rid += 1;

	$("div#" + id + " .count").html(rowCount + 1);

	$.ajax({type: "POST",
		    url: "/actions/IncrementRow.do",
		    data: {"id": id, "rid" : rid},
		    success: onIncrement
		    })
	  }
}

function onIncrement( resp )
{
    resp = JSON.parse(resp);

    crid = rid;
    nrid = parseInt(resp['rid']);

    if (nrid == crid)
	{
	    $("div#" + id + " .count").html(resp['row']);
	}
}

function getRow()
{
    var rowNode = document.getElementById('_row');
    iCount = parseInt(rowNode.value);
    return iCount;
}

