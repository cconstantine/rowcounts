google.load("jquery", "1.4.2");

function onKeyDown( evt , id)
{
    var keynum = (window.event)?evt.keyCode:evt.which;

    if (keynum==32) {
	rowCount = parseInt( $("div.count").html() );
	$("div.count").html(rowCount + 1);

	$.ajax({type: "POST",
		    url: "/actions/IncrementRow.do",
		    data: "id=" + id,
		    success: onIncrement
		    })
	  }
}

function onIncrement( newRow )
{
    cRow = parseInt($("div.count").html());
    $("div.CounterMessage").html('Hit space to increment count ' +
				 '(Expected ' +
				 cRow + ')');

    cRow = parseInt($("div.count").html());
    nRow = parseInt(newRow);

    if (nRow > cRow)
	{
	    $("div.count").html(newRow);
	}
}

function getRow()
{
    var rowNode = document.getElementById('_row');
    iCount = parseInt(rowNode.value);
    return iCount;
}

