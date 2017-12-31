function getSelectedTheme() {
    var theme = null;
    $('.themes input').each(function () {
        if (this.checked) {
            theme = this.value;
            return false;
        }
    });
    return theme;
}

function getQueryArgs(locSearch) {
    locSearch = locSearch || window.location.search;
    var args = {};

    locSearch.replace(/(\w+)=(.+?)(&|$)/g, function (substr, key, value) {
        args[key] = window.decodeURIComponent(value);
    });
    return args;
}

function getCurrentDocument() {
    return getQueryArgs()['n'];
}


function setPreviewHtml(html) {
    var iframe = $('#browse')[0];
    var doc = iframe.document;

    if (iframe.contentDocument) {
        doc = iframe.contentDocument; // For NS6
    } else if (iframe.contentWindow) {
        doc = iframe.contentWindow.document; // For IE5.5 and IE6
    }
    doc.open();
    doc.writeln(html);
    doc.close();
    var body = doc.body;

    var titleText = null;
    var headElem = $('h1', body)[0] || $('h2', body)[0] || $('h3', body)[0] || $('h4', body)[0] || $('h5', body)[0] || $('p', body)[0];
    if (headElem) {
        titleText = headElem.innerText || headElem.textContent;
    }
    if (titleText) {
        $('head title').html(titleText.substr(0, 55) + ' - ' + window.baseTitle);
    } else {
        $('head title').html(window.baseTitle);
    }
}

function getScrollHeight($prevFrame) {
    // Different browsers attach the scrollHeight of a document to different
    // elements, so handle that here.
    if ($prevFrame[0].scrollHeight !== undefined) {
        return $prevFrame[0].scrollHeight;
    } else if ($prevFrame.find('html')[0].scrollHeight !== undefined &&
        $prevFrame.find('html')[0].scrollHeight !== 0) {
        return $prevFrame.find('html')[0].scrollHeight;
    } else {
        return $prevFrame.find('body')[0].scrollHeight;
    }
}


$(function startsNewFile() {
    $('#btn-new_file').click(function () {
        $('#filename').attr("style", "display:block");
        $('#new-file-title').attr("style", "display:block");
        var clicked = $(this);
        clicked.attr("style", "display:none");
    })
})

$(function starsNewProject() {
    $('#btn-new-project').click(function () {
        var clicked = $(this);
        clicked.attr("style", "display:none");
        $('#projectname').attr("style", "display:block");
        $('#create-new-project').attr("style", "display:block");
    })
    $('#create-new-project').click(function () {
        var projectname = $("#projectname").val();
        /*var url = document.location.href+"/?project="+projectname;*/
        var url = script_root + '/?theme=' + getSelectedTheme() + '&project=' + projectname
        $.ajax({
            'url': url,
            'type': "GET",
            'success': function (response) {
                window.location = url;
            }
        })
    })
})

function delFile(nomeprogetto, nomefile) {
    if (arguments[1]) {
        result = confirm('Do you want delete' + " " + arguments[1] + "?")
    } else {
        result = confirm('Do you want delete' + " " + arguments[0]) + "?"
    }
    if (result) {
        $.ajax({
            'url': script_root + '/srv/delete/',
            'type': 'POST',
            'data': {'rst': $('textarea#editor').val(), 'project': nomeprogetto, 'filename': nomefile},
            'success': function (response) {
                window.location = '/'
            }
        })
    }
}

/**
 * syncScrollPosition
 *
 * Synchronize the scroll positions between the editor and preview panes.
 * Specifically, this function will match the percentages that each pane is
 * scrolled (i.e., if one is scrolled 25% of its total scroll height, the
 * other will be too).
 */
function syncScrollPosition() {
    var $ed = $('textarea#editor');
    var $prev = $('#browse');

    var editorScrollRange = ($ed[0].scrollHeight - $ed.innerHeight());
    var previewScrollRange = (getScrollHeight($prev.contents()) - $prev.innerHeight());

    // Find how far along the editor is (0 means it is scrolled to the top, 1
    // means it is at the bottom).
    var scrollFactor = $ed.scrollTop() / editorScrollRange;

    // Set the scroll position of the preview pane to match.  jQuery will
    // gracefully handle out-of-bounds values.
    $prev.contents().scrollTop(scrollFactor * previewScrollRange);
}

var activeXhr = null;
var lastContent = null;

function genPreview() {
    var self = $('textarea#editor');
    var rstContent = self.val();
    if (activeXhr || lastContent == rstContent) {
        //activeXhr.abort();
        return;
    }
    lastContent = rstContent;
    activeXhr = $.ajax({
        'url': script_root + '/srv/rst2html/',
        'data': {'rst': rstContent, 'theme': getSelectedTheme()},
        'type': 'POST',
        'error': function (xhr) {
            setPreviewHtml(xhr.responseText);
        },
        'success': function (response) {
            setPreviewHtml(response);
            syncScrollPosition();
            activeXhr = null;
        }
    });
}

var timerId = null;

function getCurrentLink(res) {

    if (!res) {
        return '//' + window.location.host + script_root + '/?theme=' + getSelectedTheme() + '&project=' + $.urlParam('project');
    }
    return '//' + window.location.host + script_root + '/?n=' + res + '&theme=' + getSelectedTheme() + '&project=' + $.urlParam('project');
}

function adjustBrowse() {
    var h = $('body').height() - $('#browse').offset().top - $('#footer').outerHeight() - 7;
    $('#browse').height(h);
    h -= 12;
    $('#editor').height(h).css('max-height', h + 'px');
}

$.urlParam = function (name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results == null) {
        return null;
    }
    else {
        return results[1] || 0;
    }
}


$(function () {
    //$('<button>Conver!</button>').click(genPreview).appendTo($('body'));

    window.baseTitle = $('head title').text();

    $('textarea#editor').bind('change', genPreview).markItUp(mySettings);
    timerId = window.setInterval(genPreview, 900);
    window.setTimeout(function () {
        $('#editor-td > div').css({'width': '100%', 'height': '96%'});
    }, 200);

    $('textarea#editor').scroll(syncScrollPosition);

    $('.themes input').bind('change', function () {
        lastContent = null;
        genPreview();
    });

    $.ajax({
        'url': script_root + '/srv/projects/',
        'type': 'GET',
        'data': {},
        'success': function (response) {
            for (item of response['projects']) {
                selected = '';
                if (item === $.urlParam('project')) {
                    selected = 'class="selected"';
                }
                $('.projects-list').append('<li id="project-' + item + ' " ' + selected + '><a href="#">' + item + '</a><button onclick="delFile(\'' + $.urlParam('project') + '\', \'' + item + '\')" id="delete">X</button><ul id="file-list-' + item + '" class="file-list"></ul></li>');
            }
            if ($.urlParam('project')) {
                $.ajax({
                    'url': script_root + '/srv/files/',
                    'type': 'GET',
                    'data': {'project': $.urlParam('project')},
                    'success': function (response) {
                        for (item of response['files']) {
                            $('#file-list-' + $.urlParam('project')).append('<li id="file-' + item + ' " ><a href="#">' + item + '</a> <button id="delite_file" onclick="delFile(\'' + $.urlParam('project') + '\', \'' + item + '\')" id="delete">X</button></li>');
                        }
                    }

                });
            }
        }
    });


    $('body').on('click', '.projects-list > li > a', function (e) {
        e.preventDefault();
        document.location.href = script_root + '?project=' + e.target.innerHTML;
    });

    $('body').on('click', '.file-list > li > a', function (e) {
        e.preventDefault();
        $.ajax({
            'url': script_root + '/srv/load_file/',
            'type': 'GET',
            'data': {'project': $.urlParam('project'), 'filename': e.target.innerHTML},
            'success': function (response) {
                $(e.target).parent('li').siblings().removeClass('selected');
                $(e.target).parent('li').addClass('selected');
                $("#filename").val(e.target.innerHTML);
                $('textarea#editor').val(response['content']);
            }
        })
    });

    $('#save_file').click(function (e) {
        if (!$('#filename').val()) {
            alert('Provide a file name!');
        }
        if (!$.urlParam('project')) {
            alert('Provide a project!');
        }
        $.ajax({
            'url': script_root + '/srv/save_file/',
            'type': 'POST',
            'data': {
                'rst': $('textarea#editor').val(),
                'project': $.urlParam('project'),
                'filename': $('#filename').val()
            },
            'success': function (response) {
                $('#file-list-' + $.urlParam('project')).html('');
                for (item of response['files']) {
                    selected = '';
                    if (item === $('#filename').val()) {
                        selected = 'class="selected"';
                    }
                    $('#file-list-' + $.urlParam('project')).append('<li ' + selected + ' id="file-' + item + ' " ><a href="#" >' + item + '</a></li>');
                }
            }

        });

        e.preventDefault();
        return false;
    });

    $('#save_link').click(function (e) {
        $.ajax({
            'url': script_root + '/srv/save_rst/',
            'type': 'POST',
            'data': {'rst': $('textarea#editor').val()},
            'success': function (response) {
                window.location = getCurrentLink(response + '');
                $('textarea#editor').focus();
            }

        });

        e.preventDefault();
        return false;
    });


    $('#del_link').click(function (e) {
        $.ajax({
            'url': script_root + '/srv/del_rst/',
            'type': 'GET',
            'data': {'n': getCurrentDocument()},
            'success': function (response) {
                window.location = getCurrentLink();
            }
        });

        e.preventDefault();
        return false;
    });

    $('#as_pdf').click(function (e) {
        var form = $('#save_as_pdf');
        $('#as_pdf_rst').attr('value', $("#editor").val());
        $('#as_pdf_theme').attr('value', getSelectedTheme());
        form.submit();

        e.preventDefault();
        return false;
    });

    adjustBrowse();

    $(window).bind('resize', adjustBrowse);

});
