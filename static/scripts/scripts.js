
$(document).ready(function () {
    $('.loader').hide();

    // Homepage form
    $('#new_file').click(function (e) {
        e.preventDefault();;
        console.log('Hello');
        $('.spinner-border').show();
        $('#new_form').submit();

    });

    $('#exercise').keyup(function () {
        let answerText = $('#exercise').text();
        console.log('Answer text: ', answerText);
    });

    $('#form_solution').click(function (e) {
        e.preventDefault();

        let answerText = $('#exercise').text();
        $('#student_answer').val(answerText);

        $('form').submit();
    });

    // Retrieve transcript
    $('#retrieve').click(function (e) {
        e.preventDefault();
        let data = $(this).data();
        let file_id = data.file_id;
        let position = data.position;
        $('.spinner-border').show();
        $.post(`/_retrieve/${file_id}/${position}`, function (data) {
            // TODO: Don't know why this isn't working with jQuery, but this is simple enough for vanilla JS
            document.getElementById('retrieve').parentNode.parentNode.innerHTML = data;
            // Keep the "seconds available" up to date...
            $('#seconds_available').text(Math.floor(parseInt($('#seconds_available').text()) - $('audio')[0].duration));
            $('.spinner-border').hide();

        });

    });
    // Control the speed of the player
    $('#formControlRange').change(function () {
        let audio = $('audio')[0];
        let rate = $(this).val();
        audio.playbackRate = rate;
        console.log('rate: ', rate);
        $('#playerSpeed').text(rate * 100);
    });

  // Only works on the POST solution view
  $('#exercise').height($('#solution').height());

});


