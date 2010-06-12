google.load("jquery", "1.4.2");

function onKeyDown( evt , id)
{
    var keynum = (window.event)?evt.keyCode:evt.which;
    
    if (keynum==32) {
	$.ajax({type: "POST",
		    url: "/actions/IncrementRow.do",
		    data: "id=" + id,
		    success: onIncrement
		    })
	  }
}

function onIncrement( newRow )
{
    current_row = $("div.count").html();

    $("div.count").html(newRow);
    $("div.CounterMessage").html('Hit space to increment count ' +
				 '(Previous ' +
				 current_row + ')');
}

function getRow()
{
    var rowNode = document.getElementById('_row');
    iCount = parseInt(rowNode.value);
    return iCount;
}

