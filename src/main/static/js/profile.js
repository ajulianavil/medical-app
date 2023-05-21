function editProfile(){
    var form = document.getElementById('profile-form');
    var fields = form.getElementsByTagName('input');

    for (var i = 0; i < fields.length; i++) {
        if (fields[i].name === "cedula" || fields[i].name === "email" || fields[i].name === "rol") {
            continue;
        }
      fields[i].disabled = false;
    }

    document.getElementById('editButton').style.display = 'none';
    document.getElementById('sendButton').style.display = 'flex';
} 