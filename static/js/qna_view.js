$(function() {
    $("div.thank a").click(function() {
        thank_btn = $(this);
        $.ajax({
            url: '/answer/' + thank_btn.attr('data-answer-id') + '/thank/',
            success: function() {
                thank_btn.parent().addClass("sent");
                thank_btn.parent().html("<span>• 感谢已发出</span>");
            }
        });
        return false;
    });
});
