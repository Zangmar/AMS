function query_employee_info() {
    // 查询name的在职employee
    var name = $('#employee').val()
    $.ajax({
        url: "/api/v1/employee/query_employee_info",
        type: "get",
        data: { "name": name, "is_work": '1' },
        success: function (data) {
            var html = ''
            if (data.Result == 'success') {  // json头大写
                var employee_list = data.Resp
                if (employee_list.length > 0) {
                    for (var employee of employee_list) {
                        html += `<option value='${employee.id}'>
                        ${employee.name} ${employee.department} ${employee.phone}</option>`
                    }
                }
                else {
                    html = `<option value=></option>`
                }
                $('#employee_select').html(html)
            }
            else {
                alert("ERROR: query failed!")
            }
        }
    });
    return false
}


function query_types_name(type_select_id) {
    // 查询子类型
    // type_select_id: 类型下拉框定位
    $.ajax({
        url: "/api/v1/assets/query_types_name",
        type: "get",
        success: function (data) {
            var html = '<option>---</option>'
            if (data.Result == 'success') {
                var types_list = data.Resp
                if (types_list.length > 0) {

                    for (var type of types_list) {
                        html += `<option>${type}</option>`
                    }
                }
                $(`#${type_select_id}`).html(html)
            }
            else {
                alert("ERROR: query failed!")
            }
        }
    });
    return false
}


function query_assets_name(type_select_id, asset_select_id) {
    // 查询资产名
    // type_select_id: 类型下拉框定位
    // asset_select_id: html id 设备下拉框定位
    type_name = $(`#${type_select_id}`).val()  // type_nanme: 设备名
    if (type_name == '---') {
        return false
    }
    else {
        $.ajax({
            url: "/api/v1/assets/query_assets_name",
            type: "get",
            data: { "name": type_name },
            success: function (data) {
                var html = ''
                if (data.Result == 'success') {
                    var assets_list = data.Resp
                    if (assets_list.length > 0) {
                        for (var assets of assets_list) {
                            html += `<option value="${assets.id}">${assets.name}</option>`
                        }
                    }
                    else {
                        html = `<option value=""></option>`
                    }
                    $(`#${asset_select_id}`).html(html)
                }
                else {
                    alert("ERROR: query failed!")
                }
            }
        });
        return false
    }
}


function check_phone() {
    // 1 先去隐藏警告的p并且删除submit的disabled
    // 2 检查手机号是否合法输入
    // 3 动态检查phone是否有重复
    var phone = $('#phone').val()  // 先获取phone的string
    // 1
    $("#registered_p").hide()
    $("#length_p").hide()
    $("#check_submit").removeAttr("disabled")
    // 2
    if (phone.length != 11) {
        $("#length_p").show()
        $("#check_submit").attr("disabled", "disabled")
        return false
    }
    // 3
    $.ajax({
        url: "/api/v1/employee/check_phone",
        type: "get",
        data: { "phone": phone },
        success: function (data) {
            if (data.Result == 'success' & data.Resp == 'exist') {  // json头大写
                $("#registered_p").show()
                $("#check_submit").attr("disabled", "disabled")
            }
        }
    });
    return false
}


function delete_info(apply_id) {
    // 删除操作
    $("#delete_id").attr("value", apply_id)
}


$(function () {
    // modal hide时重置表单
    // 清空addApply模态框
    $('#addApplyModal').on('hidden.bs.modal', function () {
        $('#addApplyModal input').removeAttr('value')
        $('#assets_select').empty()  // 清空assets_select
        $('#employee_select').empty()  // 清空employee_select
    });
});


$(function () {
    // 清空addApplyEmployee模态框
    $('#addApplyEmployeeModal').on('hidden.bs.modal', function () {
        $('#addApplyEmployeeModal input').removeAttr('value')
        $('#assets_select2').empty()  // 清空assets_select
    });
})


$(function () {
    // 重置删除modal
    $('#deleteApplyModal').on('hidden.bs.modal', function () {
        $('#deleteApplyModal input').removeAttr('value')
    })
})