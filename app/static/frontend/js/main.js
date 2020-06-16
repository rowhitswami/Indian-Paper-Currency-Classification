$(document).ready(function () {
  
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

  $('[data-toggle="tooltip"]').tooltip()

  if (localStorage.getItem('consent') === null) {
    $(".consent-box").show(200);
  }

  $("#consent").click(function () {
    localStorage.setItem('consent', true);
    $(".consent-box").hide(200);
  })

  $("#camera-upload").click(function () {
    $(this).hide()
    $("#click").show()
    $("#reset-camera").show()
    Webcam.set({
      width: $("#image").width(),
      height: $("#image").height(),
      image_format: 'jpeg',
      jpeg_quality: 100
    });
    Webcam.attach('#image');
  })

  $("#click").click(function () {
    $(this).hide()
    $("#reset-camera").hide()
    $("#camera-upload").show()
    Webcam.snap(function (data_uri) {
      $("#image").removeAttr("style")
      var clicked_image = '<img class="img-fluid z-depth-2 rounded" src="' + data_uri + '"/>'
      $("#image").html(clicked_image);
    });
  })

  $("#reset-camera").click(function () {
    Webcam.reset('#image');
    $(this).hide()
    $("#click").hide()
    $("#camera-upload").show()
    $("#image").removeAttr("style")
    default_image = "<img src='/static/frontend/images/placeholder.jpg' class='z-depth-2 img-fluid rounded' alt='placeholder'>"
    $("#image").html(default_image);
  })

  $("#file-upload").change(function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        var content = '<img class="img-fluid z-depth-2 rounded" src="' + e.target.result + '"/>'
        $("#image").html(content);
      }
      reader.readAsDataURL(this.files[0]);
    }
  });

  $('#upload-file-btn').click(function () {
    if ($("#image video").length == 1) {
      toastr.error("Please take a snapshot.", "Streaming video!")
      return false
    }

    var ImageURL = $("#image img").attr('src');

    if (ImageURL.split(".")[1] == "jpg") {
      toastr.error("Please select an image to upload.", "No file chosen!")
      return false
    }
    // Split the base64 string in data and contentType
    var block = ImageURL.split(";");
    // Get the content type of the image
    var contentType = block[0].split(":")[1]; // In this case "image/gif"
    // get the real base64 content of the file
    var realData = block[1].split(",")[1]; // In this case "R0lGODlhPQBEAPeoAJosM...."

    var ext = contentType.split("/")[1]
    var image_name = Math.random().toString(36).substring(4) + "." + ext

    // Convert it to a blob to upload
    var blob = b64toBlob(realData, contentType);

    var form_data = new FormData($('#upload-file')[0]);
    form_data.set("file", blob, image_name);
    $ajaxPost(form_data)
  });

  $ajaxPost = function (form_data) {
    $("#overlay").show(200)
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
        $getChart(response.labels, response.data)
      },
      error: function (response) {
        $("#overlay").hide(200)
        toastr.error(response.responseJSON.error, response.statusText)
      }
    });
  };

  $getChart = function (labels, data) {
    data.forEach((value, index) => {
      data[index] = (data[index] * 100).toFixed(2);
    });
    $("#barChart").remove()
    var canv = document.createElement('canvas');
    canv.id = 'pieChart';
    canv.height = '280';
    $("#chart").html(canv);
    var ctxB = canv.getContext('2d');
    var pieChart = new Chart(ctxB, {
      plugins: [ChartDataLabels],
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: ["#F7464A", "#46BFBD", "#ffc107", "#303f9f", "#4D5360", "#1976d2", "#4caf50"],
          hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#ffca28", "#3949ab", "#616774", "#1e88e5", "#66bb6a"]
        }]
      },
      options: {
        title: {
          display: true,
          text: "Probability of Predictions",
          fontSize: '17'
        },
        responsive: true,
        legend: {
          position: 'right',
          labels: {
            padding: 20,
            boxWidth: 10,
            fontSize: 15
          }
        },
        plugins: {
          datalabels: {
            formatter: (value, ctxB) => {
              let percentage = parseFloat(value).toFixed(2);
              return (percentage < 5) ? null : percentage+"%";
            },
            color: 'white',
            labels: {
              title: {
                font: {
                  size: '13'
                }
              }
            }
          }
        }
      }
    });
  }

  /**
   * Convert a base64 string in a Blob according to the data and contentType.
   * 
   * @param b64Data {String} Pure base64 string without contentType
   * @param contentType {String} the content type of the file i.e (image/jpeg - image/png - text/plain)
   * @param sliceSize {Int} SliceSize to process the byteCharacters
   * @see http://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript
   * @return Blob
   */
  function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      var slice = byteCharacters.slice(offset, offset + sliceSize);

      var byteNumbers = new Array(slice.length);
      for (var i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }

      var byteArray = new Uint8Array(byteNumbers);

      byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, {
      type: contentType
    });
    return blob;
  }

});