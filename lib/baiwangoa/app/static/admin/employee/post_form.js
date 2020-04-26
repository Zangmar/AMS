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

function edit_info(...rest) {
    // 更新操作
    var [id, name, phone, entry_time, department, is_work, permission] = rest
    // 更新员工信息
    // 更新form method
    $("#form_post").attr("action", "/admin/employee/update")
    // disableed phone
    $('#phone').attr('disabled', 'disabled')
    // disabled password
    $('#password').attr('disabled', 'disabled')
    // 基本数据
    $("#id").attr("value", id)
    $("#name").attr("value", name)
    $("#phone").attr("value", phone)
    $("#entry_time").attr("value", entry_time)
    $("#department").attr("value", department)

    $(`#permission_${permission}`).attr("checked", "checked")
    $(`#permission_${permission}`).attr("value", permission)

    $(`#is_work_${is_work}`).attr("checked", "checked")
    $(`#is_work_${is_work}`).attr("value", is_work)
}


function delete_info(employee_id) {
    // 删除操作
    $("#delete_id").attr("value", employee_id)
}


$(function () {
    // modal hide时重置表单
    $('#addEmployeeModal').on('hidden.bs.modal', function () {
        $("#form_post").attr("action", "/admin/employee/add")
        $('#addEmployeeModal input').removeAttr('value')
        $('#addEmployeeModal input').removeAttr('disabled')
        $('#addEmployeeModal input').removeAttr('checked')
        $('#addEmployeeModal').removeAttr('selected')
    });
});


$(function () {
    // 重置删除modal
    $('#deleteEmployeeModal').on('hidden.bs.modal', function () {
        $('#deleteEmployeeModal input').removeAttr('value')
    })
})