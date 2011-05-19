/*
$(function() {
    function sort_by_count() {
        $("ul#universities li").sortElements(function(a, b) {
            acount = $("#qcount", a).text();
            bcount = $("#qcount", b).text();
            if (acount == bcount)
                return $(a).text() > $(b).text() ? 1 : -1;
            else
                return acount < bcount ? 1 : -1;
        });
    }
    sort_by_count();

    $("a#sort_by_count").click(function() {
        sort_by_count();
        $("ul#universities").hide().fadeIn();
        return false;
    });

    $("a#sort_by_title").click(function() {
        $("ul#universities li").sortElements(function(a, b) {
            return $(a).text() > $(b).text() ? 1 : -1;
        });
        $("ul#universities").hide().fadeIn();
        return false;
    });
});
*/
