function query_assets_info(assets_dict_id, status) {
    // 查询全部入库assets_info的id与sn
    $.ajax({
        url: "/api/v1/assets/query_assets_info",
        type: "get",
        data: { "assets_dict_id": assets_dict_id, "status": status},
        success: function (data) {
            // data: [{}]
            if (data.Result == 'success') {
                assets_info_list = data.Resp
                if (assets_info_list.length > 0) {
                    var option = ''
                    for (var assets_info of assets_info_list) {
                        option += `<option value='${assets_info.id}'>${assets_info.code}</option>`
                    }
                }
                else {
                    option = `<option value=""></option>`
                }
                $("#assets_info_id").html(option)
            }
            else {
                alert("ERROR: query failed!")
            }
        }
    });
}


function edit_info(...rest) {
    // 处理申请操作
    var [apply_id, assets_dict_id, assets_dict_name, employee_id, employee_name, employee_department] = rest
    // 填充信息
    // 基本数据
    $("#apply_id").attr("value", apply_id)
    $("#assets_dict_name").attr("value", assets_dict_name)
    $("#employee_id").attr("value", employee_id)
    $("#employee_name").attr("value", employee_name)
    $("#employee_department").attr("value", employee_department)
    // query 全部入库的 assets_info
    query_assets_info(assets_dict_id, 1)  // 1:  入库
}


function delete_info(apply_id) {
    // 删除操作
    $("#delete_id").attr("value", apply_id)
}


$(function() {
    // modal hide时重置表单
    $('#addDeviceModal').on('hidden.bs.modal', function() {
        $('#handleApply input').removeAttr('value')
        $('#handleApply select').removeAttr('select')
        $('#handleApply').removeAttr('checked')
        $('#assets_info_id').empty()  // 清空select
    });
});


$(function(){
    // 重置删除modal
    $('#deleteApplyModal').on('hidden.bs.modal', function() {
        $('#deleteApplyModal input').removeAttr('value')
    })
})

