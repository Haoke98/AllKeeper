//需要先引入'kindeditor4.1.11/kindeditor-all.js','kindeditor4.1.11/lang/zh-CN.js' 和  'js/jquery-3.6.0.min.js',
KindEditor.ready(function (k) {
    window.editor = k.create('#id_Introduce', {
        resizeType: 1,
        allowPreviewEmoticons: false,
        allowImageRemote: false,
        uploadJson: '/upload/kindeditor',
        width: '800px',
        height: '400px',
    });
});


window.onload = function () {
    activatePopupInfo();
}

function activatePopupInfo() {
    let els = $('.info')//x是一个列表，element标签元素列表
    for (const el of els) {
        let id = $(el).attr('data-id');
        getInfo(id, function (info) {
            $(el).popup({
                position: 'right center',
                //     // target   : '.test.image',
                // title: title,
                content: info
            });
        })

    }
}

function getInfo(id, onSuccess) {
    $.ajax({
        url: "https://web.izbasar.link/api2/account/info",
        type: "GET",
        data: {
            id: id,
        },
        async: true,
        success: function (res) {
            if (res.status === 20000) {
                onSuccess(res.data)
            } else {
                onSuccess(res.msg)
            }
        },
        fail: function (res) {
            console.log("failed:", res)
        },
        complete: function (res) {

        }
    })
}