/*!
 * Pardus
 * Guillaume BONNET, Romain MUNOS
 */

/* Fonction pour fixer le pied de page en bas si la taille du corps de page est inférieure à la taille du navigateur */

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
    /* Appelle la fonction stickyFooter() lorsque la page est prête */
    stickyFooter();
});

$(window).resize(function () {
    /* Appelle la fonction stickyFooter() lorsque le navigateur est redimensionné */
    stickyFooter();
});