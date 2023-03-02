$(document).ready(function () {

    $("#loading").css("display", "none");

    $('form').submit(function() {
        $("#loading").css("display", "block");
        $("#form-submit").css("display", "none");
    });

});