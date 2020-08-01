$(document).ready(function () {
    "use strict";
    $(".mobile-menu").on("click", function () {
        $(this).toggleClass("open"),
        $("header nav > ul").slideToggle("slow")
    });
    document.addEventListener("touchstart",function () { },!0),
    $(window).load(function () {
        $(".loader").fadeOut("slow");
        $(".portfolio-masonry").isotope({
            itemSelector: ".selector"
        });
        $(function () {
            var t = $(".portfolio-masonry").isotope({
                itemSelector: ".item"
            }),e = {
                numberGreaterThan50: function () {
                    var t = $(this).find(".number").text();
                    return parseInt(t, 10) > 50
                },
                ium: function () {
                    var t = $(this).find(".name").text();
                    return t.match(/ium$/)
                }
            };
            $("#filters").on("click", "li", function () {
                var i = $(this).attr("data-filter");
                i = e[i] || i,
                t.isotope({
                    filter: i
                })
            });
            $(".filters").each(function (t, e) {
                var i = $(e);
                i.on("click", "li",
                function () {
                    i.find(".active").removeClass("active"),
                    $(this).addClass("active")
                })
            })
        })
    })
    $('#search-input').hide();

    $("#search-icon").on("click", function(e){
    $("#search-input").show();

    $(document).one("click", function(){
        $("#search-input").hide();
    });

    e.stopPropagation();
    });


    $("#search-input").on("click", function(e){
        e.stopPropagation();
    });


});