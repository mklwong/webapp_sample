var query_filter = {}
window.onload = extract_filter()

function change_state_list(state_list){
    var i;
    var elem = document.getElementById("state_list");
    for (i = 0; i<state_list.length; i++){
        var option = document.createElement("option");
        option.text = state_list[i];
        elem.add(option);
    }
}

function change_state_list(state_list){
    var i;
    var elem = document.getElementById("state_list");
    for (i = 0; i<state_list.length; i++){
        var option = document.createElement("option");
        option.text = state_list[i];
        elem.add(option);
    }
}

function compile_filter_payload(){
    return payload
}

function extract_filter(){
    var payload = compile_filter_payload()
    var payload_str = JSON.stringify(payload)
    $.ajax({
        url: '/get_filter',
        type: "POST",
        data: payload_str,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            query_filter = data
            change_state_list(Object.keys(data['location']))
        },
        error: function(error){
            console.log('extract_filter_error')
        }
    })
}

