var InstructorCourseSchePanel = {

    render: function (c_section) {
        Handlebars.registerPartial('course_sche_col_days', $("#course_sche_col_days").html());
        Handlebars.registerPartial('course_sche_col_bldg', $("#course_sche_col_bldg").html());
        var source = $("#instructor_course_sche_panel").html();
        var template = Handlebars.compile(source);
        c_section.netid = window.user.netid;
        if (c_section.meetings.length > 0) {
            for (var i = 0; i < c_section.meetings.length; i++) {
                c_section.meetings[i].curriculum_abbr = c_section.curriculum_abbr;
                c_section.meetings[i].course_number = c_section.course_number;
                c_section.meetings[i].section_id = c_section.section_id;

                if (!c_section.wont_meet &&
                    !c_section.no_meeting &&
                    c_section.meetings[i].type !== c_section.section_type &&
                    c_section.meetings[i].type !== 'NON') {
                    c_section.meetings[i].display_type = true;
                }
            }
        }

        var raw = template(c_section);
        $('#instructor_sche_on_course_card' + c_section.index).html(raw);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.InstructorCourseSchePanel = InstructorCourseSchePanel;
