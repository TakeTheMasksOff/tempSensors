
$(document).ready(function () {
// document.addEventListener("load", function () {
    
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('sensors', function (msg) {
        var parsed_obj = JSON.parse(msg)
        // get a new date (locale machine date time)
        var date = new Date();
        // get the date as a string
        var n = date.toDateString();
        // get the time as a string
        var time = date.toLocaleTimeString();

        // log the date in the browser console
        console.log("****************************")
        console.log('date & time:', n, " ", time);
        console.log(parsed_obj);
        console.log("============================")
        $(".last-update").html('Last update time: ' + n + " " + time)

        if (parsed_obj.AHU1_intake) {
            $(".device .in-value .value").removeClass("warning");
            $(".device .in-value .value").html(parsed_obj.AHU1_intake);
        }else {
            $(".device .in-value .value").addClass("warning");
            $(".device .in-value .value").html("X");
        }

        if (parsed_obj.AHU1_supply) {
            $(".device .out-value .value").removeClass("warning");
            $(".device .out-value .value").html(parsed_obj.AHU1_supply);
        }else {
            $(".device .out-value .value").addClass("warning");
            $(".device .out-value .value").html("X");
        }

        if (parsed_obj.AHU1_mid) {
            $(".device .middle .round-border").removeClass("warning");
            $(".device .middle .round-border").html(parsed_obj.AHU1_mid);
        }else {
            $(".device .middle .round-border").addClass("warning");
            $(".device .middle .round-border").html("X");
        }



        if (parsed_obj.AHU2_intake) {
            $(".device-2 .in-value .value").removeClass("warning");
            $(".device-2 .in-value .value").html(parsed_obj.AHU2_intake);
        }else {
            $(".device-2 .in-value .value").addClass("warning");
            $(".device-2 .in-value .value").html("X");
        }

        if (parsed_obj.AHU2_supply) {
            $(".device-2 .out-value .value").removeClass("warning");
            $(".device-2 .out-value .value").html(parsed_obj.AHU2_supply);
        }else {
            $(".device-2 .out-value .value").addClass("warning");
            $(".device-2 .out-value .value").html("X");
        }

        if (parsed_obj.AHU2_mid) {
            $(".device-2 .middle .round-border").removeClass("warning");
            $(".device-2 .middle .round-border").html(parsed_obj.AHU2_mid);
        }else {
            $(".device-2 .middle .round-border").addClass("warning");
            $(".device-2 .middle .round-border").html("X");
        }


        if (parsed_obj.AHU3_intake) {
            $(".device-3 .in-value .value").removeClass("warning");
            $(".device-3 .in-value .value").html(parsed_obj.AHU3_intake);
        }else {
            $(".device-3 .in-value .value").addClass("warning");
            $(".device-3 .in-value .value").html("X");
        }

        if (parsed_obj.AHU3_supply) {
            $(".device-3 .out-value .value").removeClass("warning");
            $(".device-3 .out-value .value").html(parsed_obj.AHU3_supply);
        }else {
            $(".device-3 .out-value .value").addClass("warning");
            $(".device-3 .out-value .value").html("X");
        }

        if (parsed_obj.AHU3_mid) {
            $(".device-3 .middle .round-border").removeClass("warning");
            $(".device-3 .middle .round-border").html(parsed_obj.AHU3_mid);
        }else {
            $(".device-3 .middle .round-border").addClass("warning");
            $(".device-3 .middle .round-border").html("X");
        }


        if (parsed_obj.AHU4_intake) {
            $(".device-4 .in-value .value").removeClass("warning");
            $(".device-4 .in-value .value").html(parsed_obj.AHU4_intake);
        } else {
            $(".device-4 .in-value .value").addClass("warning");
            $(".device-4 .in-value .value").html("X");
        }

        if (parsed_obj.AHU4_supply) {
            $(".device-4 .out-value .value").removeClass("warning");
            $(".device-4 .out-value .value").html(parsed_obj.AHU4_supply);
        } else {
            $(".device-4 .out-value .value").addClass("warning");
            $(".device-4 .out-value .value").html("X");
        }

        if (parsed_obj.AHU4_mid) {
            $(".device-4 .middle .round-border").removeClass("warning");
            $(".device-4 .middle .round-border").html(parsed_obj.AHU4_mid);
        } else {
            $(".device-4 .middle .round-border").addClass("warning");
            $(".device-4 .middle .round-border").html("X");
        }

        if (parsed_obj.device_outside) {
            $(".outside-temp").removeClass("warning");
            $(".outside-temp").html(parsed_obj.device_outside);
        } else {
            $(".outside-temp").addClass("warning");
            $(".outside-temp").html("X");
        }
    });

});