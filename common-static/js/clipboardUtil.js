function copyWithElement(item, str) {
    console.log('this is clicked item:', item);
    copyStr(str)
    $(item).popover({content:"fuck you!"})
}

function copyFromElementAttr(item, attr) {
    console.log('this is clicked item:', item);
    copyStr(item.getAttribute(attr))
    $(item).modal()
}

function copyStr(str) {
    var oInput = document.createElement('input');
    oInput.value = str;
    document.body.appendChild(oInput);
    oInput.select(); // 选择对象
    document.execCommand("Copy"); // 执行浏览器复制命令
    oInput.className = 'oInput';
    oInput.style.display = 'none';
    app.$message({
          message: '复制成功！',
          type: 'success'
    });
}