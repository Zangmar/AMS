function change_args_name() {
    // 根据select更新filter_name
    var filter_name = $('#filter_name').val()
    $('#filter_value').attr('name', filter_name)
}