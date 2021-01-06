let currentPageHost = $("#host").text();

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
    console.log(path);
    setPathText(path);
    loadNodes(path);
}

function changeActive(fullPath){
    let target = fullPath.split('/').pop() + '+';
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
            let row = '<tr><th scope="row">' + k + '</th><td>' + v + '</td></tr>'
            html += row
        });
        html = '<table class="table"><thead><tr><th scope="col">Name</th><th scope="col">Value</th></tr></thead><tbody>' + html + '</tbody></table>'
        $("#nodeData").html(html)
        changeActive(fullPath);
    });
}

function loadNodes(fullPath){
    $.ajax({
        url: "/node",
        data: {h: currentPageHost, p: fullPath}
    }).done(function(data){
        let html = '<ul class="list-group">';
        $.each(data[1], function(k, v){
            html += '<li id="' + v + '" class="list-group-item d-flex justify-content-between align-items-center" onclick="showData(\'' + v + '\')">'
            html += '<a>' + v.split('/').pop() + '</a>';
            html += '<a href="#" onclick ="setPathText(\'' + v + '\');loadNodes(\'' + v + '\')" class="badge badge-secondary">+</a>'
            html += '</li>';
        });
        html += '</ul>';
        $("#nodeList").html(html);
    })
}

$(document).ready(function(){
    setPathText('/');
    loadNodes('/');
});
