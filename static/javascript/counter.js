google.load("jquery", "1.4.2");

var rid = 0;

function onKeyDown( evt , id)
{
    var keynum = (window.event)?evt.keyCode:evt.which;

    if (keynum==32) {
	rowCount = parseInt( $("div.count").html() );
	rid += 1;

	$("div.count").html(rowCount + 1);
	$("div.rid").html(rid);

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
	    $("div.count").html(resp['row']);
	}
}

function getRow()
{
    var rowNode = document.getElementById('_row');
    iCount = parseInt(rowNode.value);
    return iCount;
}

