$(document).ready(function () {
  Sentry.init({
    dsn: 'https://5737f2ff4a084bb9a525d5b5f7f5ea85@o397473.ingest.sentry.io/5252172'
  });
  toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-bottom-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "500",
    "hideDuration": "100",
    "timeOut": "3000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }

  if (localStorage.getItem('consent') === null) {
    $(".consent-box").show(200);
  }

  $("#consent").click(function() {
    localStorage.setItem('consent', true);
    $(".consent-box").hide(200);
  })

  $('#file-upload').change(function () {
    var file = $('#file-upload')[0].files[0]
    if (typeof (file) != 'undefined')
      $(".file-path").text(file.name)
    else
      $(".file-path").text('No file chosen')
  });

  $('#upload-file-btn').click(function () {
    var file = $('#file-upload')[0].files[0]
    if (typeof (file) == 'undefined') {
      console.log("Coming here!!")
      toastr.error("Please select an image to upload.", "No file chosen!")
      return false
    }
    $("#overlay").show(200)
    var form_data = new FormData($('#upload-file')[0]);
    var upload_progress = "<div data-preset='stripe' class='overlay-content' id='progress-bar'></div>";
    $("#overlay").html(upload_progress)
    var progress_bar = new ldBar("#progress-bar");
    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", function (evt) {
          if (evt.lengthComputable) {
            var percentComplete = (evt.loaded / evt.total) * 100;
            progress_bar.set(percentComplete)
            if (percentComplete >= 100) {
              var content = "<div class='overlay-content'>"
              content += "<img src='../static/frontend/images/processing.gif' width=300>"
              content += "<h4>Processing your image!<h4></div>"
              $("#overlay").html(content);
              percentComplete = 0
            }
          }
        }, false);
        return xhr;
      },
      type: 'POST',
      url: '/',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      success: function (response) {
        $("#overlay").hide(200)
        $populateData(response)
      },
      error: function (response) {
        $("#overlay").hide(200)
        toastr.error(response.responseJSON.error, response.statusText)
      }
    });
  });

  $populateData = function (response) {
    var image = document.createElement("IMG");
    image.src = response.image_url;
    image.className = "img-fluid z-depth-2 rounded";
    $("#image").html(image);
    $("#prediction").text(response.prediction)
    $getChart(response.labels, response.data)
  }

  $getChart = function (labels, data) {
    data.forEach((value, index) => {
      data[index] = (data[index] * 100).toFixed(2);
    });
    $("#barChart").remove()
    var canv = document.createElement('canvas');
    canv.id = 'barChart';
    $("#chart").html(canv);
    var ctxB = canv.getContext('2d');
    var myBarChart = new Chart(ctxB, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: '%',
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
  }
});