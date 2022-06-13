$(document).ready(function () {
    $("#dm1").change(function () {
        $.ajax({
            url: "static/auto_2.php",
            type: "GET",
            data: 'stu_id=' + $("#dm1").val()
        })
            .success(function (result) {
                var obj = jQuery.parseJSON(result);
                
                if (obj == '') {
                    $('input[type=text]').val('');
                    $("#Name").val('');
                    $("#Surname").val('');
                }
                else {
                    $.each(obj, function (key, inval) {

                        $("#Name").val(inval["Name"]);
                        $("#Surname").val(inval["Surname"]);

                    });
                }

            });

    });

});