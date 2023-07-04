window.addEventListener("load" , function (){
    $("#top_submit").on("click", () => {
        sendPostTweet($("#top_post_form"));
    });
    $("#right_submit").on("click", () => {
        sendPostTweet($("#right_post_form"));
    });
    $("#follow_timeline").on("click", (e) => {
        if ($("#post_data").data("view_timeline") === "follow") return;
        setTimeline(e, "follow");
    });
    $("#all_timeline").on("click", (e) => {
        if ($("#post_data").data("view_timeline") === "all") return;
        setTimeline(e, "all");
    });
    window.addEventListener("scroll", ()=>{
        // $(".postform.pc").css("top",window.scrollY+"px");
        $("#post_data").data("get_next_post");
        let next = $("#post_data").data("get_next_post") == "True";
        if ((0 >= (document.body.scrollHeight - window.scrollY - document.body.clientHeight)) && next) {
            getAdditionalPosts();
            $("#post_data").data("get_next_post","False");
        }
    });
});



function setTimeline(e, select){
    let data = {
        select:select
    }
    const url     = $("#posts_dropdown").data("set_timeline_url");
    sendPostForm(url,data,(data, status, xhr) => {
        if (data.content.timeline) {
            $("#timeline").html(data.content.timeline);
        }
    });
}

function sendPostTweet(form){
    const data = new FormData(form.get(0));

    const url     = form.prop("action");
    const method  = form.prop("method");

    form.find("#post_text").val("");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 
        if (data.error){
            console.log("ERROR");
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        }
        if (data.content.timeline) {
            $("#timeline").html(data.content.timeline);
        }
        if (data.content.messages) {
            $("#messages").html(data.content.messages);
        }

    }).fail( function(xhr, status, error) {
        console.error(status + ":" + error );
    }); 
}

function getAdditionalPosts() {
    let data = {
        post_limit:$("#post_data").data("last_post_index")
    }
    
    const url = $("#post_data").data("get_additional_post_url");
    sendPostForm(url,data,(data, status, xhr) => {
        if (data.content.timeline) {
            duringCommunication = false;
            $("#timeline").html(data.content.timeline);
        }
    });
}

function clickDeletePostBtn(e) {
    const url = $(e.target).data("delete_post_url");
        let data = {
            "post_id":$(e.target).data("delete_post_no")
        }
        sendPostForm(url,data,(data, status, xhr) => {
            if (data.content.timeline) {
                $("#timeline").html(data.content.timeline);
            }
        });
}

function sendPostFollow(e,eventValue) {
    const url = $(e.target).data("follow_post_url");
    let data = {
        "event":eventValue
    }
    sendPostForm(url,data,(data, status, xhr) => {
        if (data.content.timeline) {
            $("#timeline").html(data.content.timeline);
        }
    });
}

function clickModalBtn(e) {
    for (const modal of $(".setting-modal")) {
        if ($(e.target).next()[0] !== $(modal)[0]) {
            $(modal).addClass("d-none");
        }
    }
    $(e.target).next().toggleClass("d-none");
}