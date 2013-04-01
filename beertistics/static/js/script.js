$(document).ready(function() {

    $.getJSON('/json/profile', function(user) {
        $('#user-info img').attr('src', user.avatar);
        $('#user-info a').text(user.name);
        $('#user-info a').attr('href',user.url);
    });

});