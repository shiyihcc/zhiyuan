$(function() {
    $("#university-all").click(function() {
        $("#university-list li").fadeIn();
        $(this).hide();
        $("#sort-by-count").show();
        $("#sort-by-name").show();
        return false;
    });
    $("#tag-all").click(function() {
        $("#tag-list li").fadeIn();
        $(this).hide();
        return false;
    });

    $("#sort-by-count").click(function() {
        $("#university-list li").sortElements(function(a, b) {
            return parseInt($(a).attr("data-order-count")) > parseInt($(b).attr("data-order-count")) ? 1 : -1;
        });
        $("#university-list").hide().fadeIn();
        return false;
    });

    $("#sort-by-name").click(function() {
        $("#university-list li").sortElements(function(a, b) {
            return parseInt($(a).attr("data-order-name")) > parseInt($(b).attr("data-order-name")) ? 1 : -1;
        });
        $("#university-list").hide().fadeIn();
        return false;
    });
});
