function query_employee_info() {
    // 查询name的在职employee
    var name = $('#employee').val()
    $.ajax({
        url: "/api/v1/employee/query_employee_info",
        type: "get",
        data: { "name": name, "is_work": '1' },
        success: function (data) {
            var option = ''
            if (data.Result == 'success') {  // json头大写
                var employee_list = data.Resp
                if (employee_list.length > 0) {
                    for (var employee of employee_list) {
                        option += `<option value='${employee.id}'>${employee.name} ${employee.department} ${employee.phone}</option>`
                    }
                }
                else {
                    option = `<option></option>`
                }
                $('#employee_select').html(option)
            }
            else {
                alert("ERROR: query failed!")
            }
        }
    });
    return false
}


function query_types_name() {
    // 查询子类型
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
                $('#types_select').html(html)
            }
            else {
                alert("ERROR: query failed!")
            }
        }
    });
    return false
}


function query_assets_name() {
    // 查询资产名
    type_name = $('#types_select').val()
    var html = ''
    if (type_name == '---') {
        $('#assets_select').html(html)
    }
    else {
        $.ajax({
            url: "/api/v1/assets/query_assets_name",
            type: "get",
            data: { "name": type_name },
            success: function (data) {
                if (data.Result == 'success') {
                    var assets_list = data.Resp
                    if (assets_list.length > 0) {

                        for (var assets of assets_list) {
                            html += `<option value="${assets.id};${assets.code}">${assets.name}</option>`
                        }
                    }
                    else {
                        html = `<option value=""></option>`
                    }
                    $('#assets_select').html(html)
                }
                else {
                    alert("ERROR: query failed!")
                }
            }
        });
        return false
    }
}


function check_code() {
    // 检查新建device的code是否存在
    var id_pre_code = $('#assets_select').val()
    var pre_code = id_pre_code.split(';')[1]
    var last_code = $('#last_code').val()
    var code = pre_code + '-' + last_code
    $.ajax({
        url: "/api/v1/assets/check_code",
        type: "get",
        data: { "code": code },
        success: function (data) {
            if (data.Result == 'success' & data.Resp == 'exist') {  // json头大写
                $("#registered_p").show()
                $("#registered_submit").attr("disabled", "disabled")
            }
            else {
                $("#registered_p").hide()
                $("#registered_submit").removeAttr("disabled")
            }
        }
    });
    return false
}


// 检查更新device的code是否存在
// global x
var first_code = true
var global_code = ''
function check_code_update() {
    var code = $('#code').val()
    // 先保存默认的code
    if (first_code == true) {
        global_code = code
        first_code = false
    }
    // 只有code不为默认值采取ajax请求查询
    if (code != global_code) {
        // ajax
        $.ajax({
            url: "/api/v1/assets/check_code",
            type: "get",
            data: { "code": code },
            success: function (data) {
                if (data.Result == 'success' & data.Resp == 'exist') {  // json头大写
                    $("#registered_p_update").show()
                    $("#registered_submit_update").attr("disabled", "disabled")
                }
                else {
                    $("#registered_p_update").hide()
                    $("#registered_submit_update").removeAttr("disabled")
                }
            }
        });
    }
    return false
}


function edit_info(...rest) {
    // 更新操作
    var [id, code, sn, location, status, employee_id, employee_name, employee_department, employee_phone, specifications] = rest
    // 更新员工信息
    // 基本数据
    $("#id").attr("value", id)
    $("#code").attr("value", code)
    $("#sn").attr("value", sn)
    $("#location").attr("value", location)
    // $("#status").attr("value", status)
    if (status == '3') {
        $("#status_repair").attr('checked', 'checked')
        $("status_repair").attr('value', status)
    }
    else {
        $("#status_none").attr('checked', 'checked')
        $("status_none").attr('value', '')
    }
    $("#employee").attr("value", employee_name)
    $("#employee_select").html(`<option value='${employee_id}'>
                                ${employee_name} ${employee_department} ${employee_phone}</option>`)
    $("#specifications").val(specifications)
}


function upload_file() {
    // 上传文件
    var formData = new FormData();
    formData.append("file_stream", document.getElementById("file_id").files[0]); 
    formData.append("define_name", "device");
    $.ajax({
        url: "/api/v1/upload",
        type: "post",
        data: formData,
        contentType: false,  // 发送文件需要置为false
        processData: false,  // 发送文件需要置为false
        success: function (data) {
            if (data.Result == 'success') {  // json头大写
                
                $('#upload_submit_id').removeAttr('disabled')
                $('#upload_button_id').attr('disabled', 'disabled')
                $('#file_id').attr('disabled', 'disabled')
                
                var filename = data.Resp
                $('#upload_filename_id').attr('value', filename)

                $('#upload_p_id').attr('class', 'text-success')
                var text_p = '上传成功'
            }
            else {
                var text_p = '上传失败'
                $('#upload_p_id').attr('class', 'text-danger')
            }
            $('#upload_p_id').text(text_p)
        }
    });
    return false

}


function delete_info(device_id) {
    // 删除操作
    $("#delete_id").attr("value", device_id)
}


$(function () {
    // modal hide时重置表单
    // 重置add表单
    $('#addDeviceModal').on('hidden.bs.modal', function () {
        $('#addDeviceModal input').removeAttr('value')
        // $('#addDeviceModal select').removeAttr('disabled')
        $('#addDeviceModal').removeAttr('checked')
        $('#addDeviceModal').removeAttr('selected')
    });
});


$(function () {
    // 重置update表单
    $('#updateDeviceModal').on('hidden.bs.modal', function () {
        $('#updateDeviceModal input').removeAttr('value')
        // $('#updateDeviceModal select').removeAttr('disabled')
        $('#updateDeviceModal').removeAttr('checked')
        $('#updateDeviceModal').removeAttr('selected')
        $('#employee_select').empty()
    });
})


$(function () {
    // 重置删除modal
    $('#deleteDeviceModal').on('hidden.bs.modal', function () {
        $('#deleteDeviceModal input').removeAttr('value')
    })
})


$(function () {
    // 重置上传modal
    $('#uploadModal').on('hidden.bs.modal', function () {
        $("#upload_submit_id").attr("disabled", "disabled")
        $('#upload_button_id').removeAttr('disabled')
        $('#file_id').removeAttr('disabled')

        $('#upload_p_id').removeAttr('class')
        $('#upload_p_id').text('请上传文件')

        $('#upload_filename_id').removeAttr('value')
    })
})

