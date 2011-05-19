$(function() {
    blackboard_state = $.cookie('blackboard');
    if (!blackboard_state) {
        $.cookie('blackboard', 1);
        $("#blackboard").show();
    }
    else if (blackboard_state == -1) {
        hide_blackboard();
    }

    $("#toggle_blackboard").click(function() {
        blackboard_state = $.cookie('blackboard');
        if (blackboard_state == -1)
            show_blackboard();
        else
            hide_blackboard();
        $.cookie('blackboard', -$.cookie('blackboard'));
        return false;
    });

    function hide_blackboard() {
        $("#note").attr('id', 'note-blackboard-hidden');
        $("#blackboard").hide();
        $("#toggle_blackboard").html("▼");
    }

    function show_blackboard() {
        $("#note-blackboard-hidden").attr('id', 'note');
        $("#blackboard").show();
        $("#toggle_blackboard").html("▲");
    }
});
