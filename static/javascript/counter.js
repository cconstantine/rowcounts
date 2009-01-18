
function onKeyDown( evt )
{
  var keynum = (window.event)?evt.keyCode:evt.which;
  var iCount = 0;
  if (keynum==32) {
    var _div = document.getElementById('_text');
    var rowNode = document.getElementById('_row');
    iCount = parseInt(rowNode.value) + 1;
    
    _div.childNodes[0].nodeValue = iCount;
    
    rowNode.value = iCount;
  }
}

function setMessage( message )
{
  var node = document.getElementById('spaceCounter');
  node.childNodes[0].nodeValue=message;
}
