var BasicAuth = {
    init: function (username, password) {
        return "Basic " + Base64.encode(username + ":" + password)
    },
    openBt: function (url, baUsername, baPassword) {
        $.ajax({
            type: 'GET',
            url: url,
            headers: {
                'Authorization': this.init(baUsername, baPassword)
            },
            success: function () {
                window.open(url, "_blank")
            }
        })
    }
}