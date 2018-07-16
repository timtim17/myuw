var InterStudentCard = {
    name: 'InterStudentCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.is_j1 && !window.user.is_f1) {
            $("#InterStudentCard").hide();
            return;
        }
        InterStudentCard._render();
    },

    _render: function () {
        var data = {
            is_f1: window.user.is_f1,
            is_j1: window.user.is_j1,
            seattle: window.user.seattle,
            bothell: window.user.bothell,
            tacoma: window.user.tacoma
            };
        InterStudentCard._render_with_context(data);
        LogUtils.cardLoaded(InterStudentCard.name, InterStudentCard.dom_target);
    },

    _render_with_context: function (context){
        var source = $("#international_student_card_content").html();
        var internationalStudents_template = Handlebars.compile(source);
        var raw = internationalStudents_template(context);
        InterStudentCard.dom_target.html(raw);
    },
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.InterStudentCard = InterStudentCard;
