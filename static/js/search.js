$(function() {
    keyword = $("#kw").html();
    $("div.content li").each(function() {
        var kwregexp = new RegExp(keyword, "g");
        $(this).html($(this).html().replace(kwregexp, '<span class="kw">' + keyword + "</span>"));
    });
});
