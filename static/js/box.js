function is_int(val) {
    return Math.floor(val) == val ? true : false;
}

function placeholder(object) {
    var text = object.val();
    object.focus(function() {
        if (object.val() == text) {
            object.val('');
        }
    });
    object.blur(function() {
        if (object.val() == '') {
            object.val(text);
        }
    });
}

$(function() {
    placeholder($("#shortcutform #qid"));
    placeholder($("#searchform #q"));

    $("#shortcutform").submit(function() {
        id = $("#shortcutform #qid").val();
        if (!is_int(id)) {
            alert('请输入正确的问答编号，应该是一个整数。');
            return false;
        }
        else if (!id) {
            alert('请输入问答编号。');
            return false;
        }
        window.location.href = '/view/' + id + '/';
        return false;
    });

    $("#searchform").submit(function() {
        kw = $("#searchform #q").val();
        if (is_int(kw) && kw != '211' && kw != '985') {
            window.location.href = '/view/' + kw + '/';
        }
        else if (kw == '') {
            alert('请输入一个关键词以便查询。');
        }
        else if (kw == '关键词') {
            alert('请把“关键词”三字改为你想搜索的内容，比如“小语种”等，谢谢。');
        }
        else if (kw.length >= 20) {
            alert('为了最好的搜索效果，请尝试短一些的关键词，谢谢。');
        }
        else if (
        kw.indexOf(' ') > -1 ||
        kw.indexOf('+') > -1 ||
        kw.indexOf('　') > -1 ) {
            alert('为了最好的搜索效果，请仅搜索一个关键词，谢谢。');;
        }
        else {
            window.location.href = '/search/' + kw + '/';
        }
        return false;
    });
});
