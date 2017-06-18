/**
 * Created by Administrator on 2017/6/2.
 */
function table(requestUrl) {


// {#    / 为字符串创建format方法，用于字符串格式化#}
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };
    function initialize() {
        $.ajax({
            url: requestUrl,
            type: 'GET',
            dataType: 'JSON',
            success: function (arg) {
                // arg = JSON.parse(arg);
                // {#                console.log(arg);#}
                //ajax请求 拿到httprespon的内容
                initGlobal(arg.gloab_config);
                initTableHeader(arg.table_config);
                initTableData(arg.table_config, arg.table_data);
            }
        })
    }

    GLOBAL_DICT = {};
    function initGlobal(gloab_config) {
        /**
         source_choirce = (
         (0,'B28'),
         (1,'B2C'),
         (2,'大数据'),
         (3,'开发测试'),
         (4,'运维开发'),
         )
         */

        $.each(gloab_config, function (k3, v3) {
            GLOBAL_DICT[k3] = v3;
            // {#            console.log('ALL', GLOBAL_DICT);#

        })
    }

    function initTableHeader(table_config) {
        var tr = document.createElement('tr');

        $.each(table_config, function (k, v) {
            // {#            console.log(v.display);#

            if (v.display) {
                var th = document.createElement('th');
                th.innerHTML = v.title;
                $(tr).append(th);
            }
        });
        $('#salt_tbHead').append(tr)
    }

    function initTableData(table_config, table_data) {
        $.each(table_data, function (k, row) {
            var tr = document.createElement('tr');
            //这里使用table_config的value 然后再去table_data里get取
            //table_config的q的value是把数据库的字段，是得知数据才写上去,
            //table_data是已经从数据库取到的数据,-我这里是把数据库取到的对象都放回到salt_run_json 页面中,具体数据去这个页面看  通过字段把数据库中的数据取过来，
            //table_dat, table_config   这2个数据源有个相同的值 就是字段
            //row[v1.q] 取到数据库的每一行的 每一列数据
            $.each(table_config, function (k1, v1) {
                // console.log('table_config',  v1);
                if (v1.display) {
                    var kv = {};
                    $.each(v1.type.kwargs, function (k2, v2) {
                        if (v2.substring(0, 2) == '@@') {
                            //temp 就是table_config 配置的字段
                            var temp = v2.substring(2, v2.length);
                            if (v1.q == 'source') {
                                var db_value = getDisplayByid(row.source, temp);
                                kv[k2] = db_value;
                            }
                            else if (v1.q == 'saltrun__statues') {
                                var db_value = getDisplayByidStatus(row.saltrun__statues, temp);
                                kv[k2] = db_value;
                                console.log('status', row['saltrun__statues']);
                                if (row['saltrun__statues'] === null) {
                                    var db_value = '第一次配置';
                                    kv[k2] = db_value;
                                }
                            }
                        }
                        //  var db_value = getDisplayByid(row.source, temp);
                        // kv[k2] = db_value;

                        // var db_value_status = getDisplayByidStatus(row.saltrun__statues, temp);
                        // console.log(temp);

                        // kv[k2] = db_value_status;
                        // console.log('kv',kv,'k2',k2)

                        else if (v2[0] == '@') {
                            var temp = v2.substring(1, v2.length);
                            var db_value = row[temp];
// {#                            console.log(temp);#}
                            kv[k2] = db_value;
// {#                            console.log(kv)#}
                        }
                        else {
                            kv[k2] = v2
                        }
                    });
                    var text = v1.type.tpl.format(kv);
                    var td = document.createElement('td');
                    td.innerHTML = text;
                    $(tr).append(td);
                }

            });
            $('#salt_tbBody').append(tr);
        })
    }

    function getDisplayByid(id, globalKeyname) {
// {#        console.log(id,globalKeyname,GLOBAL_DICT);#}
//         console.log('ALL', GLOBAL_DICT[globalKeyname]);
        var text = '';
        $.each(GLOBAL_DICT[globalKeyname], function (k4, v4) {
            // console.log('111',v4, id);
            if (id == v4[0]) {
                text = v4[1];
                return
            }

        });
        return text;
    }

    function getDisplayByidStatus(id, globalKeyname) {
        var text = '';
        $.each(GLOBAL_DICT[globalKeyname], function (k4, v4) {
            // console.log('111',v4, id);
            if (id == v4[0]) {
                text = v4[1];
                return
            }

        });
        return text;
    }

    initialize();
    $('#check_add').click(function () {
        // $(this).parent().siblings().find(".test").removeClass("hide")
        //   if($('.test').hasClass('hide')){
        //        $('.test').removeClass('hide');
        //    }else{
        //        $('.test').addClass('hide');
        //    }
        $('.check_add_hide').toggleClass('hide');
    });
    $('#do_delete').click(function () {
        // $(this).parent().siblings('#modal_delete').removeClass('hide');
        $('#modal_delete').toggleClass('hide');
    });
    $('#callback_delete').click(function () {
        $('#modal_delete').toggleClass('hide');

    });

}
