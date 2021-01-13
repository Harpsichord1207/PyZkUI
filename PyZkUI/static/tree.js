let currentPageHost = $("#host").text();
let deepPathICON = "+";
let activeColor = "#dbffa8";

$(document).ready(function(){
    changePath('/');
});

function changePath(path){
    setPathText(path);
    loadNodesAndActiveFirstNode(path);
}

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

function loadNodesAndActiveFirstNode(fullPath){
    $.ajax({
        url: "/node",
        data: {h: currentPageHost, p: fullPath}
    }).done(function(data){
        let html = '<ul class="list-group">';
        let firstNodeId = undefined;
        $.each(data[1], function(k, v){
            if (typeof(firstNodeId) === "undefined"){firstNodeId=v};
            html += '<li id="' + v + '" class="list-group-item d-flex justify-content-between align-items-center" onclick="changeActive(event)">'
            html += '<a class="text-break">' + v.split('/').pop() + '</a>';
            html += '<a href="#" onclick ="changePath(\'' + v + '\')" class="badge badge-success">' + deepPathICON + '</a>'
            html += '</li>';
        });
        html += '</ul>';
        $("#nodeList").html(html);
        if (typeof(firstNodeId) != "undefined"){
            $("#"+$.escapeSelector(firstNodeId)).css('background-color', activeColor);
            loadData(firstNodeId);
        };
    })
}

function changeActive(event){
    if ($(event.target).text() === deepPathICON){return}
    $("ul.list-group li").css('background-color', "");
    $(event.currentTarget).css('background-color', activeColor);
    loadData($(event.currentTarget).attr("id"));
}

function loadData(fullPath){
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
    });
}