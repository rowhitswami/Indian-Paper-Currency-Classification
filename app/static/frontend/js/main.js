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
    
    var block = ImageURL.split(";");
    var contentType = block[0].split(":")[1];
    var realData = block[1].split(",")[1];
    var ext = contentType.split("/")[1]
    var image_name = Math.random().toString(36).substring(4) + "." + ext
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
        toastr.error(response.responseJSON.error || "Please try again.", response.statusText || "Something went wrong!")
      }
    });
  };

  $getChart = function (labels, data) {
    data.forEach((value, index) => {
      data[index] = (data[index] * 100).toFixed(2);
    });
    $("#barChart").remove()
    var canv = document.createElement('canvas');
    canv.id = 'barChart';
    canv.height = '250';
    $("#chart").html(canv);
    var ctxB = canv.getContext('2d');
    var barChart = new Chart(ctxB, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: ["#8B4513", "#5b5bd2", "#c3cd32", "#ffa600", "#8a008aba", "#15f4ee", "#8d8e74"]
        }]
      },
      options: {
        title: {
          display: true,
          text: "Probability of Predictions",
          fontSize: '17',
          padding: 20
        },
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
              gridLines: {
                  display:false
              }
          }],
          yAxes: [{
              gridLines: {
                  display:false
              }   
          }]
      },
      events: false,
      tooltips: {
          enabled: false
      },
      hover: {
          animationDuration: 0
      },
      animation: {
          duration: 1,
          onComplete: function () {
              var chartInstance = this.chart,
                  ctx = chartInstance.ctx;
              ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
              ctx.textAlign = 'center';
              ctx.textBaseline = 'bottom';

              this.data.datasets.forEach(function (dataset, i) {
                  var meta = chartInstance.controller.getDatasetMeta(i);
                  meta.data.forEach(function (bar, index) {
                      var data = dataset.data[index].toString() + '%';                            
                      ctx.fillText(data, bar._model.x, bar._model.y - 5);
                  });
              });
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