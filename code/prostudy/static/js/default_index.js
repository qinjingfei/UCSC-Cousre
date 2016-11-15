// Create by Weikai Wu
// Local client to communicate with the server

// function app
// execute when the page starts
var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    self.task_exists = function (task_name) {
        var b = false;
        for (var i = 0; i < self.vue.tasks.length; i++) {
            if (self.vue.tasks[i].name==task_name){
                b = true;
                break;
            }
        }
        return b;
    };

    self.add_task = function () {
        if (self.vue.is_counting_down){ // you can't add a task while counting down
            $.post(add_conflict_url,function () {});
        }
        else if (self.vue.form_task){ // if duplicated task
            if (self.task_exists(self.vue.form_task)){
                $.post(dup_task_url,function () {})
            }
            else if (self.vue.logged_in){
                // $.post() function takes 3 params: an url, an object, and a function
                // add_task_url is defined in index.html, take a look at it
                /* in this case, $.post() sent an object has 3 fields: task_category, task_content, and task_time to the
                   add_task() function in api.py. if add_task() in api.py successfully returns, execute the function
                   specified by the 3rd param of $.post().*/
                $.post(add_task_url,
                {
                    task_category: self.vue.form_category,
                    task_content: self.vue.form_task,
                    task_time: self.vue.form_time
                },
                function (data) { // param data is returned by the python function in api.py
                    self.vue.tasks.unshift({
                        id: data.id,
                        cate: data.cate,
                        name: data.name,
                        time: data.time
                    });
                    if (self.vue.has_more) {
                        self.get_data();
                    }
                });
            }
            else { // not logged in
                // don't connect to the server and store everything locally
                self.vue.tasks.unshift({
                        id: self.vue.idx,
                        name: self.vue.form_task,
                        cate: self.vue.form_category,
                        time: self.vue.form_time * 60
                });
                self.vue.idx = self.vue.idx +1;
            }
        }
        else { // empty form
            // send to default.py to flash out "Please enter a task" message
            $.post(empty_form_url, function () {})
        }
        self.vue.form_task = null;
        self.vue.form_time = 25;
        self.vue.form_category = 'p';
        self.vue.is_adding_task = false;
        setTimeout(function () {
            self.vue.is_adding_task = true;
            $("#vue-div").show();
        },1);
        $("#vue-div").show();
    };

    self.get_data = function () {
        var start_idx = 0;
        var end_idx = 4;
        $.getJSON(get_data_url,
            {
                start_idx: start_idx,
                end_idx: end_idx
            },
            function (data) {
            self.vue.logged_in = data.logged_in;
            self.vue.has_more = data.has_more;
            self.vue.tasks = data.tasklist;
            self.vue.current_user_email = data.current_usr_email;
        })
    };

    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.get_more = function () {
        var start_idx = self.vue.tasks.length;
        var end_idx = start_idx + 4;
        $.getJSON(get_data_url,
            {
                start_idx: start_idx,
                end_idx: end_idx
            },
            function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.tasks, data.tasklist);
        });
    };

    self.delete_task = function(task_id) {
        if (self.vue.is_counting_down){ // you can't delete a task while counting down
            $.post(del_conflict_url,function () {});
            return;
        }
        if (self.vue.logged_in) {
            $.post(del_task_url, {task_id: task_id}, function () {self.get_data()});
        }
        var idx = null;
        for (var i = 0; i < self.vue.tasks.length; i++) {
            if (self.vue.tasks[i].id === task_id) {
                // If I set this to i, it won't work, as the if below will
                // return false for items in first position.
                idx = i + 1;
                break;
            }
        }
        if (idx) {
            self.vue.tasks.splice(idx - 1, 1);
            if (self.vue.selected_task_id==task_id) {
                self.vue.selected_task_id = null;
                self.vue.time_actual = 25 * 60;
                self.vue.time_countdown = '00:25:00';
            }

        }
    };

    function paddingZero(i) {
        return (i < 10)?('0' + i):i;
    }


    self.start_count_down = function () {
        if (self.vue.time_actual===0)
            return;
        self.vue.is_counting_down = true;
        self.vue.myClock = setInterval(
            function () {
                --self.vue.time_actual;
                var hr = paddingZero(Math.floor(self.vue.time_actual / 3600));
                var min = paddingZero(Math.floor(self.vue.time_actual % 3600 / 60));
                var sec = paddingZero(self.vue.time_actual % 60);
                self.vue.time_countdown = hr+':' + min + ":" + sec;
                if (self.vue.time_actual===0) {
                    clearInterval(self.vue.myClock);
                    self.time_up_twinkle();
                }
            }, 1000);
    };


    self.time_up_twinkle = function () {
        self.vue.alarm.play();
        self.vue.myTwinkle = setInterval(
            function () {
                self.vue.is_twinkling = !self.vue.is_twinkling;
            },500)
    };


    self.stop_count_down = function () {
        clearInterval(self.vue.myClock);
        clearInterval(self.vue.myTwinkle);
        self.vue.is_counting_down = false;
        self.vue.is_twinkling = false;
        self.vue.alarm.pause();
        if (self.vue.logged_in) {
            $.post(update_time_url,
                {
                    time_remained : self.vue.time_actual,
                    task_id: self.vue.selected_task_id
                },
                function () {

                }
            )
        }
        for (var i = 0; i < self.vue.tasks.length; i++) {
            if (self.vue.tasks[i].id === self.vue.selected_task_id) {
                self.vue.tasks[i].time = self.vue.time_actual;
                break;
            }
        }
    };


    self.select_task = function (task) {
        // unselect
        if (self.vue.selected_task_id == task.id) {
            self.vue.selected_task_id = null;
            self.vue.time_actual = 25 * 60;
            self.vue.time_countdown = '00:25:00';
            return;
        }
        // you can't select a task while other task is counting down
        if (!self.vue.is_counting_down){
            self.vue.selected_task_id = task.id;
            // in seconds
            self.vue.time_actual = task.time;
            // hr:min:sec
            self.vue.time_countdown = paddingZero(Math.floor(task.time / 3600))
                + ':' + paddingZero(Math.floor((task.time % 3600) / 60))
                + ':' + paddingZero(task.time % 3600 % 60);
        }

    };


    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //
            idx: 0,
            // local tasklist
            tasks: [],
            // keep track of which task is selected
            selected_task_id: null,
            // input fields
            // serve as v-model in index.html
            form_task: null,
            form_time: 25,
            form_category: 'p',
            // to show the time with time format
            time_countdown: '00:00:05',
            // actual time in seconds
            time_actual: 5,
            // console information
            logged_in: false,
            has_more: false,
            is_adding_task: true,
            is_counting_down: false,
            myClock: null,
            myTwinkle: null,
            is_twinkling: false,
            alarm: new Audio(alarm_url)
        },
        methods: {
            // functions that used in index.html, defined above
            add_task: self.add_task,
            get_data: self.get_data,
            get_more: self.get_more,
            delete_task: self.delete_task,
            select_task: self.select_task,
            // to avoid duplicate
            task_exists: self.task_exists,
            // used by get more
            extend: self.extend,
            // for countdown clock
            start_count_down: self.start_count_down,
            stop_count_down: self.stop_count_down,
            // time's up!
            time_up_twinkle: self.time_up_twinkle
        },
        computed: {

        }

    });
    self.get_data();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
