/*!
 * PARDUS
 * Guillaume BONNET, Romain MUNOS
 */


function stickyFooter() {
    var browserHeight = $(window).height();
    var bodyHeight = $("body").height();
    if (bodyHeight < browserHeight) {
        $("footer.footer").addClass("footer-bottom");
    } else {
        $("footer.footer").removeClass("footer-bottom");
    }
}

$(document).ready(function () {
    stickyFooter();
});

$(window).on("resize", function () {
    stickyFooter();
});