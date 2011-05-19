$(function() {
    $('#checkbox_selectedonly').click(function() {
        if ($('#checkbox_selectedonly').attr('checked')) {
            $('#q-list > li:not(.selected)').hide();
        }
        else {
            if ($('#checkbox_private').attr('checked')) {
                $('#q-list > li').show();
            }
            else {
                $('#q-list > li:not(.private)').show();
            }
        }
    });
    $('#checkbox_private').click(function() {
        if ($('#checkbox_private').attr('checked')) {
            if (!$('#checkbox_selectedonly').attr('checked')) {
                $('#q-list > li.private').show();
            }
        }
        else {
            $('#q-list > li.private').hide();
        }
    });
});
