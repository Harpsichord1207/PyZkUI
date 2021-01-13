let addBtn = '<button id="addBtn" type="button" class="btn btn-outline-info btn-sm" style="margin-left: 5px" data-toggle="modal" data-target="#addHostModal">+</button>'
let spinBtn = '<button id="spinBtn" class="btn btn-outline-info btn-sm" type="button" disabled><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Loading...</span></button>'

function openNodePage(hostId){
    window.location.href = "/zk?id="+hostId;
}

function showAlert(message){
    let alert = '<div class="alert alert-warning alert-dismissible fade show" role="alert">';
    alert += message;
    alert += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'
    alert += '<span aria-hidden="true">&times;</span></button></div>'
     $(".container").append(alert);
}

function generateRow(hostRow){
    let id = hostRow.id;
    let gBtn = '<button type="button" class="btn btn-outline-success btn-sm" onclick="openNodePage(' + id + ')">√</button>';
    let dBtn = '<button type="button" class="btn btn-outline-danger btn-sm" onclick="deleteHost(' + id + ')">-</button>';
    let row = '<tr><th scope="row">' + id + '</th><td>' + hostRow.host + '</td>';
    row += '<td>' + hostRow.time + '</td><td>';
    row += gBtn;
    row += dBtn;
    row += '</td></tr>';
    return row;
}

function reloadHostTable(){
    $.ajax({
        url: "/load_hosts",
        type: "get"
    }).done(function(data){
        let hostTableHtml = "";
        $.each(data, function(index, row){
            hostTableHtml += generateRow(row);
        });
        $("tbody").html(hostTableHtml);
    });
}

<!--TODO: RESTAPI-->
function deleteHost(hostId){
    $("#addBtn").remove();
    $("#titleAndButtonArea").append(spinBtn);
    $.ajax({
        url: "/delete_host",
        type: "get",
        data: {id: hostId}
    }).done(function(data){
        $("#spinBtn").remove();
        $("#titleAndButtonArea").append(addBtn);
        if (data.status == 'failed') {
            showAlert('Failed to delete hostId=' + hostId + '.')
        }
        reloadHostTable();
    })
}


$(document).ready(function(){
    $("#titleAndButtonArea").append(addBtn)
    reloadHostTable();

    $("#saveBtn").click(function(){
        let host = $("#inputHost").val() + ":" + $("#inputPort").val();
        $("#addBtn").remove();
        $("#titleAndButtonArea").append(spinBtn)
        $.ajax({
            url: "/add_host",
            type: "get",
            data: {host: host}
        }).done(function(data){
            $("#spinBtn").remove();
            $("#titleAndButtonArea").append(addBtn)
            if (data.status == 'success') {
                $("tbody").append(generateRow(data));
            } else {
                let message = '<strong>Connect Failed!</strong> Please check the host <i>' + host + '.</i>';
                showAlert(message);
            }
        });
    });
});