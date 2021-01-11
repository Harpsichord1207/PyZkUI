let currentPageHost = $("#host").text();
let deepPathICON = "+";

function setPathText(path){
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

function changePath(path){
    setPathText(path);
    loadNodes(path);
}

function defaultActive(){
    console.log($("ul.list-group").children(":first").text());
    $("ul.list-group").children(":first").css('background-color', '#dbffa8');
}


function changeActive(fullPath){
    let target = fullPath.split('/').pop() + deepPathICON;
    $("ul.list-group").children().each(function(){
        if ($(this).text() === target){
            $(this).css('background-color', '#dbffa8')
        } else {
            $(this).css('background-color', '')
        }
    });
}

function showData(fullPath){
    $.ajax({
        url: "/node",
        data: {h: currentPageHost, p: fullPath}
    }).done(function(data){
        let html = "";
        $.each(data[0], function(k, v){
            if (k!="data"){
                let row = '<tr><th scope="row">' + k + '</th><td>' + v + '</td></tr>';
                html += row;
            } else {
                 $("#nodeData").val(v);
            }
        });
        html = '<table class="table"><tbody>' + html + '</tbody></table>'
        $("#nodeInfo").html(html)
        changeActive(fullPath);
    });
}

function loadNodes(fullPath){
    $.ajax({
        url: "/node",
        data: {h: currentPageHost, p: fullPath}
    }).done(function(data){
        let firstNode = undefined;
        let html = '<ul class="list-group">';
        $.each(data[1], function(k, v){
            if (typeof(firstNode) == "undefined") { firstNode=v; }
            html += '<li id="' + v + '" class="list-group-item d-flex justify-content-between align-items-center" onclick="showData(\'' + v + '\')">'
            html += '<a class="text-break">' + v.split('/').pop() + '</a>';
            html += '<a href="#" onclick ="setPathText(\'' + v + '\');loadNodes(\'' + v + '\')" class="badge badge-success">' + deepPathICON + '</a>'
            html += '</li>';
        });
        html += '</ul>';
        $("#nodeList").html(html);
        if (typeof(firstNode) != "undefined"){ showData(firstNode); }
    })
}

$(document).ready(function(){
    changePath('/');
});
