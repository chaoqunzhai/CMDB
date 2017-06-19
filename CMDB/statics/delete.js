function delurl(requestUrl) {
    $('#do_delete_confirm').click(function () {
        $(':checkbox').each(function () {
            var v = $(this).prop('checked');
            // var v = $(':checkbox').prop('checked');
            // console.log(v);
            if (v == true) {
                // var v2 = $(':checkbox').parent().next().text();
                var v1_1 = $(this).parent().next().text();
                $.ajax({
                   url: requestUrl,
                    type:'DELETE',
                    dataType: 'JSON',
                    data:v1_1,
                    success:function (uid) {
                        location.reload()
                    }
                });
                console.log('if1', true, v1_1);
            } else if (v == false) {
                var v1_2 = $(this).parent().next().text();
                console.log('if2', false, v1_2)
            }
        });


    })

}
