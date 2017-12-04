// index of photos in slideshow
var slideIndex = 0;

// tick tock sound
var tickTock;

// sad sound
var loser;

// happy sound
var winner;

// to store user's answers in round two
var answerMapTwo = {};

// to store user's answers in round three
var answerMapThree = {};

// set timer
var secondsBeforeExpire = 28;

// list of available answers
var availableAnswers = [];

// execute when the DOM is fully loaded
$(function() {

    // Index
    // start slideshow of photos when on home page
    if ($("#index").length > 0) {
        showSlides();
    }

    // https://www.w3schools.com/howto/howto_js_slideshow.asp
    function showSlides() {

        // get all photos
        var i;
        var slides = document.getElementsByClassName("slides");

        // hide all photos
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }

        // show next photo
        slideIndex++;
        if (slideIndex > slides.length) {slideIndex = 1}
        slides[slideIndex-1].style.display = "block";

        // change photo every 3 seconds
        setTimeout(showSlides, 3000);
    }

    // Round 2
    if ($("#container").length > 0) {
        // start timer on delay
        setTimeout(function () { timerFn(); }, 3000);
    }

    // hide all questions but first
    $(".questions_two").each(function(index) {
        if (index != 0) {
            $(this).hide();
        }
    });

    // hide all years but first
    $(".year").each(function(index) {
        if (index != 0) {
            $(this).hide();
        }
    });

    // click listener on before button
    $("#before").click(function() {

        // store user's answer
        answerMapTwo[$(".questions_two:visible").text()] = $("#before").val();

        // check if next question exists
        if ($(".questions_two:visible").next().length != 0) {

            // show next question and year
            $(".questions_two:visible").next().show().prev().hide();
            $(".year:visible").next().show().prev().hide();
        }

        // disable 'next question' button when all questions completed
        else {
            $("#before").prop('disabled', true);
            $("#after").prop('disabled', true);
        }
        return false;
    });

    // click listener on after button
    $("#after").click(function() {

        // store user's answer
        answerMapTwo[$(".questions_two:visible").text()] = $("#after").val();

        // check if next question exists
        if ($(".questions_two:visible").next().length != 0) {

            // show next question and year
            $(".questions_two:visible").next().show().prev().hide();
            $(".year:visible").next().show().prev().hide();
        }

        // disable 'next question' button when all questions completed
        else {
            $("#before").prop('disabled', true);
            $("#after").prop('disabled', true);
        }
        return false;
    });

    // send answer_map as a JSON object when form submitted by user
    $('#form_two').on('submit', function() {
        $('#answer_map_two').val(JSON.stringify(answerMapTwo));
    });

    // create sound object
    function sound(src) {
        this.sound = document.createElement("audio");
        this.sound.src = src;
        this.sound.setAttribute("preload", "auto");
        this.sound.setAttribute("controls", "none");
        this.sound.style.display = "none";
        document.body.appendChild(this.sound);
        this.play = function(){
            this.sound.play();
        };
        this.stop = function(){
            this.sound.pause();
        };
    }

    // http://soundbible.com/1258-Tick-Tock.html
    tickTock = new sound("/static/timer.wav");

    // https://forums.asp.net/t/1978552.aspx?jquery+1+7+countdown+timer+i+wants+to+disable+a+button+when+the+timer+gets+zero+ -->
    function timerFn () {
        var timerVar = setInterval(function () {

            if(secondsBeforeExpire <= 0) {

                // stop tick tock sound when timer expires
                tickTock.stop();

                // disable buttons and stop timer when expires
                clearInterval(timerVar);
                $("#before").prop('disabled', true);
                $("#after").prop('disabled', true);
            }

            // otherwise display timer
            else {
                // play tick tock sound while timer running
                tickTock.play();

                // decrement time remaining
                secondsBeforeExpire--;
                $("#timer").text(secondsBeforeExpire);
            }
        }, 1000);
    }

    // Round 3
    // hide all questions but first
    $(".questions_three").each(function(index) {
        if (index != 0) {
            $(this).hide();
        }
    });

    // configure autocomplete
    $(".answers_three").each(function(index) {
        availableAnswers.push($(this).text());
    });
    $('#user_answer_three').autocomplete({
        source: availableAnswers
    });

    // send answer_map as a JSON object when form submitted by user
    $("#final_answer").click(function() {
        answerMapThree[$(".questions_three:visible").text()] = $("#user_answer_three").val();
        $("#answer_map_three").val(JSON.stringify(answerMapThree));
    });

    // Loser
    // http://soundbible.com/1830-Sad-Trombone.html
    loser = new sound("/static/loser.wav");

    if ($("#loser").length > 0) {
        loser.play();
    }

    // Winner
    // http://soundbible.com/988-Applause.html
    winner = new sound("/static/winner.wav");

    if ($("#winner").length > 0) {
        winner.play();
    }
});