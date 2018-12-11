
$(document).ready(function () {
// document.addEventListener("load", function () {
    
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('sensors', function (msg) {
        var parsed_obj = JSON.parse(msg)
        console.log(DateT);
        // get a new date (locale machine date time)
        var date = new Date();
        // get the date as a string
        var n = date.toDateString();
        // get the time as a string
        var time = date.toLocaleTimeString();

        // log the date in the browser console
        console.log('date & time:', n, " ", time);
        console.log(parsed_obj);
    });

});