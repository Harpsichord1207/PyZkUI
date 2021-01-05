let currentPageHost = $("#host").text();

function setPathText(path){
    // TODO: clickable
    $("#path").text(path);
}

function changeActive(fullPath){
    $("#nodeList").each(function(){
        console.log($(this));
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
        html = '<table class="table"><thead><tr><th scope="col">Name</th><th scope="col">Value</th></tr></thead> <tbody>' + html + '</tbody></table>'
        $("#nodeData").html(html)
        let ele = $("#"+$.escapeSelector(fullPath));
        let originAttr = ele.attr('class');
        ele.attr('class', originAttr + ' active');
        changeActive('/');
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
            html += '<a>' + v + '</a>';
            html += '<a href="#" class="badge badge-secondary">+</a>'
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
