WSData = {
    _book_data: {},
    _book_data_error_status: {},
    _category_link_data: {},
    _course_data: {},
    _course_data_error_status: {},
    _instructed_course_data: {},
    _instructed_course_data_error_status: {},
    _instructed_emaillist_data_error_status: {},
    _instructed_emaillist_data: {},
    _instructed_section_data: {},
    _instructed_section_data_error_status: {},
    _instructed_section_details: null,
    _instructed_section_details_error_status: null,
    _department_events: null,
    _grade_data: {},
    _hfs_data: null,
    _applicant_data: null,
    _mygrad_data: null,
    _iasystem_data: null,
    _library_data: null,
    _oquarter_data: null,
    _notice_data: null,
    _notice_error_status: null,
    _profile_data: null,
    _profile_error_status: null,
    _tuition_data: null,
    _directory_data: null,
    _directory_error_status: null,
    _instructor_data: {},
    _link_data: null,
    _success_callbacks: {},
    _error_callbacks: {},
    _callback_args: {},
    _academic_calendar_data: null,
    _current_academic_calendar_data: null,
    _myplan_data: {},
    _thrive_data: null,
    _upass_data: null,
    _hx_toolkit_msg: null,


    // MUWM-1894 - enqueue callbacks for multiple callers of urls.
    _is_running_url: function(url) {
        if (WSData._success_callbacks[url] && WSData._success_callbacks[url].length) {
            return true;
        }
        return false;
    },
    _enqueue_callbacks_for_url: function(url, success, error, args) {
        if (!WSData._success_callbacks[url]) {
            WSData._success_callbacks[url] = [];
            WSData._error_callbacks[url] = [];
            WSData._callback_args[url] = [];
        }
        // Even if these are null, push them so the lists stay in sync.
        WSData._success_callbacks[url].push(success);
        WSData._error_callbacks[url].push(error);
        WSData._callback_args[url].push(args);
    },

    _run_success_callbacks_for_url: function(url) {
        var i,
            callback,
            args;

        for (i = 0; i < WSData._success_callbacks[url].length; i++) {
            callback = WSData._success_callbacks[url][i];
            args = WSData._callback_args[url][i];

            if (callback) {
                callback.apply(null, args);
            }
        }

        delete WSData._success_callbacks[url];
        delete WSData._error_callbacks[url];
        delete WSData._callback_args[url];
    },

    _run_error_callbacks_for_url: function(url) {
        var i,
            callback,
            args;

        for (i = 0; i < WSData._error_callbacks[url].length; i++) {
            callback = WSData._error_callbacks[url][i];
            args = WSData._callback_args[url][i];

            if (callback) {
                callback.apply(null, args);
            }
        }

        delete WSData._success_callbacks[url];
        delete WSData._error_callbacks[url];
        delete WSData._callback_args[url];
    },

    book_data: function(term) {
        return WSData._book_data[term];
    },

    book_data_error_code: function(term) {
        return WSData._book_data_error_status[term];
    },

    course_data_error_code: function(term) {
        return WSData._course_data_error_status[term];
    },
    normalized_course_data: function(term) {
        var course_data;
        if (term) {
            course_data = WSData.course_data_for_term(term);
        } else {
            course_data = WSData.current_course_data();
        }
        if (course_data) {
            WSData._normalize_instructors(course_data);
        }
        return course_data;
    },

    current_course_data: function() {
        return WSData._course_data.current;
    },

    course_data: function() {
        if (window.console) {
            console.warn("Use WSData.current_course_data");
        }
        return WSData.current_course_data();
    },

    course_data_for_term: function(term) {
        return WSData._course_data[term];
    },

    instructed_course_data_error_code: function(term) {
        return WSData._instructed_course_data_error_status[term];
    },

    normalized_instructed_course_data: function(term) {
        var course_data;
        if (term) {
            course_data = WSData.instructed_course_data_for_term(term);
        } else {
            course_data = WSData.current_instructed_course_data();
        }

        return WSData._normalize_instructed_data(course_data);
    },

    _link_secondary_sections: function (term) {
        var course_data = WSData.instructed_course_data_for_term(term);
        if (course_data) {
            WSData._normalize_instructors(course_data);

            var linked_secondaries;
            var linked_primary_label;
            $.each(course_data.sections, function () {
                if (this.is_primary_section) {
                    // verify prev linked_secondaries
                    if (linked_secondaries &&
                        linked_secondaries.length ===0) {
                        linked_secondaries = null;
                    }

                    if (this.total_linked_secondaries) {
                        this.linked_secondaries = [];
                        linked_secondaries = this.linked_secondaries;
                        linked_primary_label = this.section_label;
                    }
                } else {
                    primary_label = this.primary_section_label;
                    if (primary_label === linked_primary_label &&
                        linked_secondaries !== undefined) {
                        this.under_disclosure = true;
                        linked_secondaries.push(this);
                    }
                }
            });
        }
        return course_data;
    },

    _normalize_instructed_data: function (course_data) {
        if (course_data) {
            WSData._normalize_instructors(course_data);

            $.each(course_data.related_terms, function () {
                this.is_current = (parseInt(window.term.year) === this.year &&
                                   window.term.quarter.toLowerCase() === this.quarter.toLowerCase());
                this.matching_term = (course_data.year === this.year &&
                                      course_data.quarter.toLowerCase() === this.quarter.toLowerCase());
            });

            var grading_is_open = course_data.grading_period_is_open;
            var grading_is_closed = course_data.grading_period_is_past;
            var grading_open = moment(course_data.term.grading_period_open);
            var grading_deadline = moment(course_data.term.grade_submission_deadline);
            var ref = moment();
            // search param supports testing
            if (window.location.search.length) {
                match = window.location.search.match(/\?grading_date=(.+)$/);
                if (match) {
                    ref = moment(decodeURI(match[1]));
                    grading_is_closed = grading_deadline.isBefore(ref);
                    grading_is_open = (!grading_is_closed && grading_open.isBefore(ref));
                }
            }

            var grading_open_relative = grading_open.from(ref);
            var grading_deadline_relative = grading_deadline.from(ref);
            var grading_open_date;
            var grading_deadline_date;

            var fmt = 'MMM D [at] h:mm A';
            var month_to_day_shift = 5;
            if (Math.abs(grading_open.diff(ref, 'days')) > month_to_day_shift) {
                grading_open_date = grading_open.format(fmt) + ' PST';
            } else {
                grading_open_date = grading_open.calendar(ref);
            }

            if (Math.abs(grading_deadline.diff(ref, 'days')) > month_to_day_shift) {
                grading_deadline_date = grading_deadline.format(fmt) + ' PST';
            } else {
                grading_deadline_date = grading_deadline.calendar(ref);
            }

            var minutes_till_open = grading_open.diff(ref, 'minutes');
            var opens_in_24_hours = (minutes_till_open >= 0 &&
                                     minutes_till_open <= (24 * 60));

            var minutes_till_deadline = grading_deadline.diff(ref, 'minutes');
            var deadline_in_24_hours = (minutes_till_deadline >= 0 &&
                                        minutes_till_deadline <= (24 * 60));
            var comparison_date = moment(window.card_display_dates.comparison_date);

            $.each(course_data.sections, function () {
                var course_campus = this.course_campus.toLowerCase();
                this.is_seattle = (course_campus === 'seattle');
                this.is_bothell = (course_campus === 'bothell');
                this.is_tacoma =  (course_campus === 'tacoma');

                this.year = course_data.year;
                this.quarter = course_data.quarter;
                this.summer_term = course_data.summer_term;
                this.future_term = course_data.future_term;
                this.past_term = course_data.past_term;

                this.registration_start = course_data.term.registration_periods[0].start;
                this.time_schedule_published = course_data.term.time_schedule_published;

                // check if the enrollment is of previous term
                var all_published = true;
                for (var campus in this.time_schedule_published) {
                    all_published = all_published && this.time_schedule_published[campus];
                    if (!all_published) { break; }
                }
                var not_published_on_course_campus = (course_campus in this.time_schedule_published &&
                                                      !this.time_schedule_published[course_campus]);
                this.is_prev_term_enrollment = false;
                if (!all_published && this.sln === 0 && not_published_on_course_campus) {
                    this.is_prev_term_enrollment = true;
                    this.prev_enrollment_year = this.year - 1;
                }

                // grading
                this.grading_period_is_open = grading_is_open;
                this.grading_period_is_past = grading_is_closed;
                this.opens_in_24_hours = opens_in_24_hours;
                this.deadline_in_24_hours = deadline_in_24_hours;
                this.grading_period_open_date = grading_open_date;
                this.grading_period_relative_open = grading_open_relative;
                this.grade_submission_deadline_date = grading_deadline_date;
                this.grade_submission_relative_deadline = grading_deadline_relative;

                if ('grading_status' in this && this.grading_status) {
                    this.grading_status.all_grades_submitted =
                        (this.grading_status.unsubmitted_count === 0);
                    if (this.grading_status.submitted_date &&
                        this.grading_status.submitted_date !== 'None') {
                        var submitted = moment(this.grading_status.submitted_date);
                        if (Math.abs(submitted.diff(ref, 'days')) > month_to_day_shift) {
                            this.grading_status.submitted_relative_date = submitted.format(fmt) + ' PST';
                        } else {
                            this.grading_status.submitted_relative_date = submitted.calendar(ref);
                        }
                    }
                }

                this.grade_submission_section_delegate = false;
                $.each(this.grade_submission_delegates, function () {
                    if (this.level.toLowerCase() === 'section') {
                        this.grade_submission_section_delegate = true;
                        return false;
                    }
                });

                // wire up eval data
                if (this.evaluation) {
                    this.evaluation.response_rate_percent = 0;
                    this.evaluation.is_past = false;
                    if (this.evaluation.response_rate) {
                        this.evaluation.response_rate_percent = Math.round(this.evaluation.response_rate * 100);
                    }
                    if (this.evaluation.eval_open_date) {
                        var eval_open = moment(this.evaluation.eval_open_date);
                        this.evaluation.eval_open_date_display = eval_open.format(fmt) + ' PST';
                        this.evaluation.is_open = comparison_date.isAfter(eval_open);
                    }
                    if (this.evaluation.eval_close_date) {
                        var eval_close = moment(this.evaluation.eval_close_date);
                        this.evaluation.eval_close_date_display = eval_close.format(fmt) + ' PST';
                        this.evaluation.is_past = comparison_date.isAfter(eval_close);
                        if (this.evaluation.is_past) {
                            this.evaluation.is_open = false;
                        }
                    }
                    if (this.evaluation.report_available_date) {
                        var report_date = moment(this.evaluation.report_available_date);
                        this.evaluation.report_available_date_display = report_date.format(fmt) + ' PST';
                        this.evaluation.report_is_available = comparison_date.isAfter(report_date);
                    }
                }
            });
        }
        return course_data;
    },

    current_instructed_course_data: function() {
        return WSData._instructed_course_data.current;
    },

    instructed_course_data_for_term: function(term) {
        return WSData._instructed_course_data[term];
    },

    instructed_section_data_error_code: function(section_label) {
        return WSData._instructed_section_data_error_status[section_label];
    },
    normalized_instructed_section_data: function(section_label) {
        var section_data = WSData.instructed_section_data(section_label);
        return WSData._normalize_instructed_data(section_data);
    },

    instructed_section_data: function(section_label) {
        return WSData._instructed_section_data[section_label];
    },

    instructed_section_details: function() {
        return WSData._instructed_section_details;
    },

    instructed_section_details_error_code: function() {
        return WSData._instructed_section_details_error_status;
    },

    grade_data_for_term: function(term) {
        if (!term) { term = ''; }
        return WSData._grade_data[term];
    },

    iasystem_data: function() {
        return WSData._iasystem_data;
    },

    hfs_data: function() {
        return WSData._hfs_data;
    },

    instructor_data: function(regid) {
        return WSData._instructor_data[regid];
    },

    library_data: function() {
        return WSData._library_data;
    },

    link_data: function() {
        return WSData._link_data;
    },

    mygrad_data: function() {
        return WSData._mygrad_data;
    },

    notice_data: function() {
        return WSData._notice_data;
    },

    oquarter_data: function() {
        return WSData._oquarter_data;
    },

    category_link_data: function(category) {
        return WSData._category_link_data[category];
    },

    tuition_data: function() {
        return WSData._tuition_data;
    },

    directory_data: function() {
        return WSData._directory_data;
    },

    profile_data: function() {
        return WSData._profile_data;
    },

    applicant_data: function(){
        return WSData._applicant_data;
    },

    dept_event_data: function() {
        return WSData._department_events;
    },
    thrive_data: function() {
        return WSData._thrive_data;
    },
    upass_data: function() {
        return WSData._upass_data;
    },

    hx_toolkit_msg_data: function(){
        return WSData._hx_toolkit_msg;
    },

    fetch_event_data: function(callback, err_callback, args) {
        if (WSData._department_events === null) {
            $.ajax({
                    url: "/api/v1/deptcal/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._department_events = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    academic_calendar_data: function() {
        return WSData._academic_calendar_data;
    },

    current_academic_calendar_data: function() {
        return WSData._current_academic_calendar_data;
    },

    myplan_data: function(year, quarter) {
        if (WSData._myplan_data[year]) {
            if (WSData._myplan_data[year][quarter]) {
                return WSData._myplan_data[year][quarter];
            }
        }
        return null;
    },

    fetch_academic_calendar_events: function(callback, err_callback, args) {
        if (!WSData._academic_calendar_data) {
            var url = "/api/v1/academic_events";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._academic_calendar_data = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_current_academic_calendar_events: function(callback, err_callback, args) {
        if (!WSData._current_academic_calendar_data) {
            var url = "/api/v1/academic_events/current/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._current_academic_calendar_data = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_book_data: function(term, callback, err_callback, args) {
        if (!WSData._book_data[term]) {
            var url = "/api/v1/book/" + term;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._book_data[term] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._book_data_error_status[term] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },


    fetch_current_course_data: function(callback, err_callback, args) {
        return WSData.fetch_course_data_for_term("current", callback, err_callback, args);
    },

    fetch_course_data_for_term: function(term, callback, err_callback, args) {
        if (!WSData._course_data[term]) {
            var url = "/api/v1/schedule/"+term;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    if (results.sections && results.sections.length &&
                        term !== 'prev_unfinished') {
                        WSData.process_term_course_data(results);
                    }
                    WSData._course_data_error_status[term] = null;
                    WSData._course_data[term] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._course_data_error_status[term] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }

    },

    process_term_course_data: function(results) {
        // MUWM-549 and MUWM-552
        $.each(results.sections, function () {
            var canvas_url = this.canvas_url;
            if (canvas_url) {
                if (this.class_website_url === canvas_url) {
                    this.class_website_url = null;
                }
                var matches = canvas_url.match(/\/([0-9]+)$/);
                var canvas_id = matches[1];
                var alternate_url = "https://uw.instructure.com/courses/"+canvas_id;

                if (this.class_website_url === alternate_url) {
                    this.class_website_url = null;
                }
            }
        });
    },

    fetch_instructed_course_data_for_term: function(term, callback, err_callback, args) {
        if (!WSData._instructed_course_data[term]) {
            var url = "/api/v1/instructor_schedule/"+term;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",
                async: true,
                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    if (results.sections && results.sections.length) {
                        WSData.process_term_course_data(results);
                    }
                    WSData._instructed_course_data_error_status[term] = null;
                    WSData._instructed_course_data[term] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._instructed_course_data_error_status[term] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }

    },

    fetch_instructed_section_data: function(section_label, callback, err_callback, args) {
        if (!WSData._instructed_section_data[section_label]) {
            var url = "/api/v1/instructor_section/" + section_label;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",
                async: true,
                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    if (results.sections && results.sections.length) {
                        WSData.process_term_course_data(results);
                    }
                    WSData._instructed_section_data_error_status[section_label] = null;
                    WSData._instructed_section_data[section_label] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._instructed_section_data_error_status[section_label] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }

    },

    fetch_instructed_section_details: function(section_label, callback, err_callback, args) {
        var url = "/api/v1/instructor_section_details/" + section_label.replace(/&amp;/g, "%26");

        if (window.section_data.hasOwnProperty('lti_session_id')) {
            url = "/lti" + url;
        }

        if (WSData._is_running_url(url)) {
            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            return;
        }

        WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

        $.ajax({
            url: url,
            dataType: "JSON",
            async: true,
            type: "GET",
            accepts: {html: "text/html"},
            success: function(results) {
                WSData._instructed_section_details_error_status = null;
                WSData._instructed_section_details = results;
                WSData._run_success_callbacks_for_url(url);
            },
            error: function(xhr, status, error) {
                WSData._instructed_section_details_error_status = xhr.status;
                WSData._run_error_callbacks_for_url(url);
            }
        });

    },

    fetch_grades_for_term: function(term, callback, err_callback, args) {
        if (!term) { term = ''; }

        if (WSData.course_data_for_term(term)) {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
            return;
        }

        $.ajax({
            url: "/api/v1/grades/"+term,
            type: 'GET',
            success: function(results) {
                WSData._grade_data[term] = results;
                err_callback.call(null, status, error);
            },
            error: function(xhr, status, error) {
                err_callback.call(null, xhr.status, error);
            }
        });
    },

    fetch_current_week_data: function(callback, err_callback, args) {
        $.ajax({
            url: "/api/v1/current_week/",
            type: 'GET',
            success: function(results) {
                callback.apply(null, [results, args]);
            },
            error: function() {
                err_callback.call(null, status, error);
            }
        });
    },

    fetch_course_data: function(callback, args) {
        console.warn("Use WSData.fetch_current_course_data instead");
    },

    fetch_link_data: function(callback, err_callback, args) {
            if (WSData._link_data === null) {
                $.ajax({
                    url: "/api/v1/links/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._link_data = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, status, error);
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },

    fetch_instructor_data: function(callback, err_callback, args) {
        var instructor_regid = args[1];
        if (WSData._instructor_data[instructor_regid] === undefined) {
            $.ajax({
                    url: "/api/v1/person/"+instructor_regid,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._instructor_data[instructor_regid] = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, status, error);
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },


    normalize_instructors_for_term: function(term) {
        WSData._normalize_instructors(WSData.course_data_for_term(term));
    },

    normalize_instructors_for_current_term: function() {
        WSData._normalize_instructors(WSData.current_course_data());
    },

    _sort_instructors_by_last_name: function(a, b) {
        if (a.surname < b.surname){
            return -1;
        }
        if (a.surname > b.surname){
            return 1;
        }
        return 0;
    },

    _normalize_instructors: function(data) {
        if (!data.sections.length) {
            return;
        }
        if (data.sections[0].instructors !== undefined) {
            return;
        }

        var section_index = 0;
        for (section_index = 0; section_index < data.sections.length; section_index++) {
            var section = data.sections[section_index];
            section.instructors = [];

            var instructors = {};
            var meeting_index = 0;
            for (meeting_index = 0; meeting_index < section.meetings.length; meeting_index++) {
                var meeting = section.meetings[meeting_index];
                var instructor_index = 0;
                for (instructor_index = 0; instructor_index < meeting.instructors.length; instructor_index++) {
                    var instructor = meeting.instructors[instructor_index];

                    if (instructors[instructor.uwregid] === undefined) {
                        section.instructors.push(instructor);
                    }
                    instructors[instructor.uwregid] = true;
                }
            }
            section.instructors = section.instructors.sort(WSData._sort_instructors_by_last_name);
        }
    },

    normalize_instructors: function() {
        if (window.console) {
            console.warn("Use WSData.normalize_instructors_for_current_term");
        }
        WSData.normalize_instructors_for_current_term();
    },

    fetch_hfs_data: function(callback, err_callback, args) {
        if (WSData._hfs_data === null) {
            $.ajax({
                    url: "/api/v1/hfs/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._hfs_data = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_iasystem_data: function(callback, err_callback, args) {
        if (WSData._iasystem_data === null) {
            var url = "/api/v1/ias/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: 'GET',
                accepts: {html: "application/json"},
                success: function(results) {
                    WSData._iasystem_data = results;
                    if (callback !== null) {
                        callback.apply(null, args);
                    }
                },
                error: function(xhr, status, error) {
                    if (err_callback !== null) {
                        err_callback.call(null, xhr.status, error);
                    }
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_library_data: function(callback, err_callback, args) {
        if (WSData._library_data === null) {
            $.ajax({
                    url: "/api/v1/library/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._library_data = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_mygrad_data: function(callback, err_callback, args) {
        if (WSData._mygrad_data === null) {
            $.ajax({
                url: "/api/v1/grad/",
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._mygrad_data = results;
                    callback.apply(null, args);
                },
                error: function(xhr, status, error) {
                    err_callback.call(null, xhr.status, error);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_tuition_data: function(callback, err_callback, args) {
        if (WSData._tuition_data === null) {
            $.ajax({
                    url: "/api/v1/finance/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._tuition_data = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_directory_data: function(callback, err_callback, args) {
        if (WSData._directory_data === null) {
            $.ajax({
                    url: "/api/v1/directory/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._directory_data = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        WSData._directory_error_status = xhr.status;
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_notice_data: function(callback, err_callback, args) {
        if (WSData._notice_data === null) {
            var url = "/api/v1/notices/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._notice_data = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._notice_error_status = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_oquarter_data: function(callback, err_callback, args) {
        if (WSData._oquarter_data === null) {
            $.ajax({
                    url: "/api/v1/oquarters/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._oquarter_data = results;
                        callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_category_links: function(callback, err_callback, args) {
        var category = args[0];
        if (WSData._category_link_data[category] === undefined) {
            $.ajax({
                    url: "/api/v1/categorylinks/" + category,
                    dataType: "JSON",
                    type: "GET",
                    accepts: {html: "application/json"},
                    success: function(results) {
                        WSData._category_link_data[category] = results;
                        callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_profile_data: function(callback, err_callback, args) {
        if (WSData._profile_data === null) {
            var url = "/api/v1/profile/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._profile_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._profile_error_status = xhr.status;
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_applicant_data: function(callback, err_callback, args) {
        if (WSData._applicant_data === null) {
            var url = "/api/v1/applications/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",
                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._applicant_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._profile_error_status = xhr.status;
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_myplan_data: function(year, quarter, callback, err_callback, args) {
        if (WSData.myplan_data(year, quarter) === null) {
            var url = "/api/v1/myplan/"+year+"/"+quarter;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    if (!WSData._myplan_data[year]) {
                        WSData._myplan_data[year] = {};
                    }
                    WSData._myplan_data[year][quarter] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_upass_data: function(callback, err_callback, args) {
        if (WSData.upass_data() === null) {
            var url = "/api/v1/upass/";
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "application/json"},
                success: function(results) {
                    WSData._upass_data = results;
                    if (callback !== null) {
                        callback.apply(null, args);
                    }
                },
                error: function(xhr, status, error) {
                    err_callback.call(null, xhr.status, error);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_hx_toolkit_week_msg: function(callback, err_callback, args) {
        WSData.fetch_hx_toolkit_msg_data(undefined, callback, err_callback, args);
    },

    fetch_hx_toolkit_msg_data: function(message_id, callback, err_callback, args) {
        if (WSData.hx_toolkit_msg_data() === null) {
            var url = "/api/v1/hx_toolkit/week/";
            if(message_id){
                url = "/api/v1/hx_toolkit/" + message_id;
            }

            $.ajax({
                url: url,
                dataType: "html",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._hx_toolkit_msg = results;
                    if (callback !== null) {
                        callback.apply(null, args);
                    }
                },
                error: function(xhr, status, error) {
                    err_callback.call(null, xhr.status, error);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    save_links: function(links) {
        var csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;
        $.ajax({
                url: "/api/v1/links/",
                dataType: "JSON",
                data: JSON.stringify(links),
                type: "PUT",
                accepts: {html: "text/html"},
                headers: {
                     "X-CSRFToken": csrf_token
                },
                success: function(results) {
                },
                error: function(xhr, status, error) {
                }
       });
    },

    mark_notices_read: function(notice_hashes) {
        var csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;
        $.ajax({
                url: "/api/v1/notices/",
                dataType: "JSON",
                data: JSON.stringify({"notice_hashes": notice_hashes}),
                type: "PUT",
                accepts: {html: "text/html"},
                headers: {
                     "X-CSRFToken": csrf_token
                },
                success: function() {
                },
                error: function(xhr, status, error) {
                }
       });
    },

    log_interaction: function(interaction_type, term) {
        var logging_term;
        if(term === undefined) {
            logging_term = "";
        }
        else {
            logging_term = "_term_" + term.replace(/[^a-z0-9]/gi, '_');
        }

        $.ajax({
                url: "/logger/" + interaction_type + logging_term,
                type: "GET",
                success: function(results) {},
                error: function(xhr, status, error) {}
        });
    },

    fetch_thrive_data: function(callback, err_callback, args) {
        if (WSData._thrive_data === null) {
            var url = "/api/v1/thrive/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._thrive_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_thrive_data_history: function(callback, err_callback, args) {
        if (WSData._thrive_data === null) {
            var url = "/api/v1/thrive/?history=1";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._thrive_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_instructed_section_emaillist_data: function(section_label, callback, err_callback, args) {
        if (!WSData._instructed_emaillist_data[section_label]) {
            var url = "/api/v1/emaillist/" + section_label;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",
                async: true,
                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._instructed_emaillist_data_error_status[section_label] = null;
                    WSData._instructed_emaillist_data[section_label] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._instructed_emaillist_data_error_status[section_label] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.WSData = WSData;
