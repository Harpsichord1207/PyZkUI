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
            let his = '<h4>History</h4><div class="list-group">' + ul + '</div>'
            $(".container").append(his)
        }
    });
}

$(document).ready(function(){
    console.log("doc ready!");
    loadHistory();
    $(".btn").click(function(){
        $(location).attr("href", "zk?h="+$(".form-control").val());
    });
});