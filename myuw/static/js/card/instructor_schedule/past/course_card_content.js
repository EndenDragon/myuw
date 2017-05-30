var InstructorPastCourseCardContent = {

    render: function (c_section, iasystem_data_resource) {
        var eval_data = iasystem_data_resource ? iasystem_data_resource.data : null;
        var index = c_section.index;
        var source = $("#instructor_past_course_card_content_panel").html();
        var template = Handlebars.compile(source);

        var raw = template(c_section);
        $('#instructor_course_card_content' + index).html(raw);

        InstructorPastCourseSchePanel.render(c_section);
        InstructorPastCourseResourcePanel.render(c_section);

        if (c_section.grade_submission_delegates) {
            CourseInstructorPanel.render(c_section);
        }
    }
};
