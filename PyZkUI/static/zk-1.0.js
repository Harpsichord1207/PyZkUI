function loadHistory() {
    $.ajax({
        url: "/his"
    }).done(function(data){
        let ul = ""
        for(i in data){
            let h = data[i];
            ul = ul + '<a href="/zk?h=' + h + '" class="list-group-item list-group-item-action">' + h + '</a>';
        }
        if (ul.length > 0) {
            $("#history").html("");
            let his = '<h4>History</h4><div class="list-group">' + ul + '</div>'
            $("#history").append(his)
        }
    });
}

function btkClick() {
    $(".btn").click(function(){
        $(location).attr("href", "zk?h="+$(".form-control").val());
    });
}


function getTree() {
    $.ajax({
        url: "/tree?h="+$("#host").text(),
        dataType: "json"
    }).done(function(treeData){
        if (treeData.status == 'success') {
            $('#tree').text("");
            $('#tree').bstreeview({data: JSON.stringify(treeData.data)});
        } else {
            $('#tree').text(treeData.message);
        }
    })
}
