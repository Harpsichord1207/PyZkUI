let currentPageHost = $("#host").text();
let deepPathICON = "+";
let activeColor = "#dbffa8";

$(document).ready(function(){
    changePath('/');
    $("#saveBtn").click(function(){
         let currentPath = $("#currentPath").val();
         let newNode = $("#nodeName").val();
         let newNodeFullPath = currentPath + "/" + newNode;
         let newNodeData = $("#newNodeData").val();
         $.ajax({
             url: "/node",
             type: "post",
             data: {h: currentPageHost, p: newNodeFullPath, d: newNodeData}
         }).done(function(data){
            if (data.status == 'success') {
                changePath(currentPath);
            } else {
                showAlert(data.message);
            };
         });
    });
    $("#deleteBtn").click(function(){
         $.ajax({
             url: "/node",
             type: "delete",
             data: {h: currentPageHost, p: $("#deletePath").val()}
         }).done(function(data){
            if (data.status == 'success') {
                changePath($("#currentPath").val());
            } else {
                showAlert(data.message);
            }
         })
    });
});


function showAlert(message){
    let alert = '<div class="alert alert-warning alert-dismissible fade show" role="alert">';
    alert += message;
    alert += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'
    alert += '<span aria-hidden="true">&times;</span></button></div>'
     $("#alertMessage").append(alert);
}

function changePath(path){
    setPathText(path);
    loadNodesAndActiveFirstNode(path);
}

function setPathText(path){
    $("#currentPath").val(path);
    if (path==="/"){
        $("#path").html('<button type="button" class="btn btn-sm btn-outline-secondary" onclick="changePath(\'' + path + '\')">/</button>');
    } else {
        let html = "";
        let incrementPath = "";
        $.each(path.split('/'), function(k, v){
            if (v===""){
                v='/';incrementPath='/'
            } else {
                if (incrementPath==='/'){incrementPath+=v;}else{incrementPath=incrementPath+'/'+v;};
            };
            html += '<button type="button" class="btn btn-sm btn-outline-secondary" onclick="changePath(\'' + incrementPath + '\')">';
            html += v + '</button>';
        });
        $("#path").html(html);
    }
}

function loadNodesAndActiveFirstNode(fullPath){
    $.ajax({
        url: "/node",
        data: {h: currentPageHost, p: fullPath}
    }).done(function(data){
        if (data.status === 'success'){
            let html = '<ul class="list-group">';
            let firstNodeId = undefined;
            $.each(data.children, function(k, v){
                if (typeof(firstNodeId) === "undefined"){firstNodeId=v};
                html += '<li id="' + v + '" class="list-group-item d-flex justify-content-between align-items-center" onclick="changeActive(event)">'
                html += '<a class="text-break">' + v.split('/').pop() + '</a>';
                html += '<a href="#" onclick ="changePath(\'' + v + '\')" class="badge badge-success">' + deepPathICON + '</a>'
                html += '</li>';
            });
            html += '</ul>';
            $("#nodeList").html(html);
            if (typeof(firstNodeId) != "undefined"){
                $("#deletePath").val(firstNodeId);
                $("#"+$.escapeSelector(firstNodeId)).css('background-color', activeColor);
                loadData(firstNodeId);
            };
        } else {
            showAlert(data.message);
        }
    })
}

function changeActive(event){
    if ($(event.target).text() === deepPathICON){return}
    $("ul.list-group li").css('background-color', "");
    $(event.currentTarget).css('background-color', activeColor);
    $("#deletePath").val($(event.currentTarget).attr("id"));
    loadData($(event.currentTarget).attr("id"));
}

function loadData(fullPath){
    $.ajax({
        url: "/node",
        data: {h: currentPageHost, p: fullPath}
    }).done(function(data){
        if (data.status === 'success'){
            let html = "";
            $.each(data.node, function(k, v){
                if (k!="data"){
                    let row = '<tr><th scope="row">' + k + '</th><td>' + v + '</td></tr>';
                    html += row;
                } else {
                     $("#nodeData").val(v);
                }
            });
            html = '<table class="table"><tbody>' + html + '</tbody></table>'
            $("#nodeInfo").html(html)
        } else {
            showAlert(data.message);
        }
    });
}