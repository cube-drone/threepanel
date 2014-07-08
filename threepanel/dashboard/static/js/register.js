
$(function(){
    
    var username_normalize = function(username){
        var slugged = username.toLowerCase().replace(/[^a-z0-9]/g, "_");
        $(".username").val(slugged);
    }
    var username_check = function(username){
        // user_exists is defined in users_bloom.js
        if(user_exists(username)){
            console.log("exists");
            $("#register .unknown").hide();
            $("#register .available").hide();
            $("#register .unavailable").show();
            $("#register .button").addClass("disabled");
        }
        else{
            console.log("doesn't exist");
            $("#register .unknown").hide();
            $("#register .available").show();
            $("#register .unavailable").hide();
            $("#register .button").removeClass("disabled");
        }
    }

    $('.username').change(function(ev){
        username_normalize($($(ev.currentTarget)[0]).val())
    });
    $('.register_username').change(function(ev){
        username_check($($(ev.currentTarget)[0]).val())
    });

});
