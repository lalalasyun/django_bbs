function clickSettingBtn() {
    const url = $("#setting").data("url");
    const data = new FormData($("#setting_form").get(0));
    sendPostForm(url,data,(data, status, xhr) => {
        if (data.content.profile) {
            $("#profile").html(data.content.profile);
        }
    });
}

function uploadImage() {
    $("#upload_form").submit();
}

function clickFollowBtn() {
    const url = $("#follow").data("url");
    const data = {
        "event":"follow"
    }
    sendPostForm(url,data,(data, status, xhr) => {
        if (data.content.profile) {
            $("#profile").html(data.content.profile);
        }
    });
}

function clickUnFollowBtn() {
    const url = $("#follow").data("url");
    const data = {
        "event":"unfollow"
    }
    sendPostForm(url,data,(data, status, xhr) => {
        if (data.content.profile) {
            $("#profile").html(data.content.profile);
        }
    });
}