function enableFields(){
    var form = document.getElementById('report-form');
    var fields = form.getElementsByTagName('input');

    for (var i = 0; i < fields.length; i++) {
        if (fields[i].name === "cedula") {
            continue;
        }
      fields[i].disabled = false;
    }

    document.getElementById('editButton').style.display = 'none';
    document.getElementById('sendButton').style.display = 'block';
} 

function saveFields(){
    document.getElementById('editButton').style.display = 'block'; 
    document.getElementById('sendButton').style.display = 'none';
}
  
function enableReportFields(){
    // var form = document.getElementById('full-report-form');
    // var fields = form.getElementsByTagName('input');

    // for (var i = 0; i < fields.length; i++) {
    //     fields[i].disabled = false;
    // }

    // document.getElementById('observaciones').style.display = 'block';
    document.getElementById("obs").disabled = false;
    document.getElementById("obs").focus();

    document.getElementById('editReport').style.display = 'none';
    document.getElementById('saveReport').style.display = 'block';
}
  
function saveReport(){
   document.getElementById('editReport').style.display = 'block';
   document.getElementById('saveReport').style.display = 'none';
 }