$(document).ready(function () {
    // get csrf-token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;
    var current = 1;
    var steps = $("fieldset").length;

    setProgressBar(current);

    $(".next").click(function () {
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        var index_fs = $("fieldset").index(next_fs) // fieldsets

        // validate steps
        if (index_fs === 1) {
            addActiveClass()
        } else if (index_fs === 2) {
            // validate shop information
            let shop_title = $('#title').val()
            let shop_location = $('#location').val()
            let shop_slug = $('#slug').val()
            let shop_about = $('#about').val()
            let shop_demand = $('#demand').val()
            let shop_supply = $('#supply').val()

            if (
                (shop_title === "" || shop_title.length <= 4) ||
                (shop_location === "" || shop_location.length <= 2) ||
                (shop_slug === "" || shop_slug.length <= 4) ||
                (shop_about === "" || shop_about.length < 5) ||
                (shop_demand === "" || shop_demand.length < 5) ||
                (shop_supply === "" || shop_supply.length < 5)
            ) {
                alert("لطفا اطلاعات خودرا به درستی وارد نمایید.")
            } else {
                $.ajax({
                    url: "/shops/register-shop/data-create",
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify({
                        payload: {
                            shop_title,
                            shop_location,
                            shop_slug,
                            shop_about,
                            shop_demand,
                            shop_supply
                        }
                    }),
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    success: (data) => {
                        if (data['status'] === 'success') {
                            addActiveClass()
                        } else if (data['status'] === 'fail') {
                            alert("ایجاد فروشگاه با خطا مواجه شد.")
                        }
                    },
                    error: (data) => {
                        alert("مشکلی پیش آمده لطفا دوباره امتحان کنید.")
                    }
                })
            }
        } else if (index_fs === 3) {
            // validate seller information
            let phone_number = $('#phone').val()
            let full_name = $('#full_name').val()
            let national_code = $('#national_code').val()

            if (
                (phone_number === "" || phone_number.length < 11 || phone_number.length > 11) ||
                (full_name === "" || full_name.length <= 4) ||
                (national_code === "" || national_code.length < 10 || national_code.length > 10)
            ) {
                alert("لطفا اطلاعات خودرا به درستی وارد نمایید.")
            } else {
                // set data
                let payload = {
                    phone_number,
                    full_name,
                    national_code
                }

                // ajax request to server
                $.ajax({
                    url: "/shops/register-shop/seller-information-create",
                    type: "POST",
                    dataType: "json",
                    data: JSON.stringify({payload}),
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    success: (data) => {
                        if (data['status'] === 'success') {
                            addActiveClass()
                        } else {
                            alert("لطفا اطلاعات خودرا به درستی وارد نمایید.")
                        }
                    },
                    error: (data) => {
                        alert("مشکلی پیش آمده لطفا دوباره امتحان کنید.")
                    }
                })
            }

        }

        //Add Class Active function
        function addActiveClass() {
            $("#progressbar li").eq(index_fs).addClass("active");

            //show the next fieldset
            next_fs.show();
            //hide the current fieldset with style
            current_fs.animate(
                {opacity: 0},
                {
                    step: function (now) {
                        // for making fielset appear animation
                        opacity = 1 - now;

                        current_fs.css({
                            display: "none",
                            position: "relative",
                        });
                        next_fs.css({opacity: opacity});
                    },
                    duration: 500,
                }
            );
            setProgressBar(++current);
        }
    });

    $(".previous").click(function () {
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //Remove class active
        $("#progressbar li")
            .eq($("fieldset").index(current_fs))
            .removeClass("active");

        //show the previous fieldset
        previous_fs.show();

        //hide the current fieldset with style
        current_fs.animate(
            {opacity: 0},
            {
                step: function (now) {
                    // for making fielset appear animation
                    opacity = 1 - now;

                    current_fs.css({
                        display: "none",
                        position: "relative",
                    });
                    previous_fs.css({opacity: opacity});
                },
                duration: 500,
            }
        );
        setProgressBar(--current);
    });

    function setProgressBar(curStep) {
        var percent = parseFloat(100 / steps) * curStep;
        percent = percent.toFixed();
        $(".progress-bar").css("width", percent + "%");
    }

    $(".submit").click(function () {
        return false;
    });
});

