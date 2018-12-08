var ALLOWED_CATEGORIES = ["plastique", "metal", "papier", "verre",
    "menage", "encombrants", "electroniques", "piles", "ampoule", "vetements", "medicaments", "carton", "humain", "cigarette"];
function sendData(url, fileName, imageFile, annotations) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify({
                'filename': fileName,
                'imageBase64': imageFile,
                'annotations': annotations
            }),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8'
        }).done(function (msg) {
            resolve();
            console.log("Data Saved: " + msg);
        }).fail(function (msg) {
            reject();
            console.log("Failed: " + msg);
        });
    });
}
function getAnnotationsForBindButton(bindButton) {
    var annotations = anno.getAnnotations(
        bindButton.prev().find('img').attr('src'));
    if (annotations.length != 0) {
        return annotations
    }
    else {
        return null;
    }
}

function isValidCategory(category) {
    if (ALLOWED_CATEGORIES.includes(category.toLowerCase())) {
        return true;
    } else {
        return false;
    }
}
function areAnnotationsValid(annotations) {
    for (var i = 0; i < annotations.length; i++) {
        if (!isValidCategory(annotations[i].text)) {
            return false;
        }
    }
    return true;
}
/*jslint unparam: true, regexp: true */
/*global window, $ */
$(function () {
    'use strict';
    function fail($this) {
        $this.text('Fail: server error, please contact to administrator.').removeClass()
            .addClass('btn btn-danger btn-block disabled');
        console.log('Fail');
    }
    function success($this) {
            $this.text('Uploaded').removeClass()
                .addClass('btn btn-success btn-block disabled');
            var linkedImage = $this.prev().find('img');
            anno.destroy(linkedImage.attr('src'));
            linkedImage.fadeOut();
            linkedImage.fadeOut("slow");
            $this.fadeOut(2000);
            $this.remove();
    }
    var upload_api = '/upload',
        uploadButton = $('<button/>')
            .addClass('btn btn-primary btn-block')
            .prop('disabled', true)
            .text('Processing...')
            .on('mouseenter', function () {
                var $this = $(this);
                var annotations = getAnnotationsForBindButton($this);
                if (!annotations) {
                    $this.removeClass().addClass('btn btn-warning btn-block')
                        .text('Annotate first');
                    return;
                }
                if (!areAnnotationsValid(annotations)) {
                    $this.removeClass().addClass('btn btn-warning btn-block')
                        .text('Category is not valid.');
                    return;
                }
                $this.removeClass().addClass('btn btn-primary btn-block')
                    .text('Upload')
                    .css('border', 'none');
            })
            .on('mouseleave', function () {
            })
            .on('click', function () {
                var $this = $(this);
                var annotations = getAnnotationsForBindButton($this);
                if (!annotations) {
                    $this.removeClass().addClass('btn btn-danger btn-block')
                        .text('Fail: No Annotatons.');
                    $this.prev().find('img')
                        .css('border', '4px solid #f44336');
                    return;
                }
                if (!areAnnotationsValid(annotations)) {
                    $this.removeClass().addClass('btn btn-danger btn-block')
                        .text('Fail: Category is not valid.');
                    return;
                }
                $this.removeClass().addClass('btn btn-info btn-block disabled')
                    .text('Uploading')
                    .prop('disabled', true);
                var imageEncoded = $this.data("imageEncoded");
                var fileName = $this.data("fileName");
                sendData(upload_api, fileName, imageEncoded, annotations)
                    .then(function () {
                        success($this);
                    }, function () {
                        fail($this);
                });
            });
    $('#fileupload').fileupload({
        url: upload_api,
        dataType: 'json',
        autoUpload: false,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 999000,
        // Enable image resizing, except for Android and Opera,
        // which actually support image resizing, but fail to
        // send Blob objects via XHR requests:
        disableImageResize: /Android(?!.*Chrome)|Opera/
            .test(window.navigator.userAgent),
        previewMaxWidth: 100,
        previewMaxHeight: 100,
        previewCrop: true
    }).on('fileuploadadd', function (e, data) {
        data.context = $('<div/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            var img = $('<img/>');
            img.attr({
                'class': 'img_preview',
                'src': URL.createObjectURL(file),
                'width': 500
            });
            img.appendTo(data.context);
            var reader = new window.FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = function () {
                var base64data = reader.result;
                var image_encoded = base64data.substr(base64data.indexOf(',') + 1);
                if (!index) {
                    uploadButton.clone(true).data({
                        "imageEncoded": image_encoded,
                        "fileName": file.name,
                    }).appendTo(data.context);
                }
            };
        });
    }).on('fileuploadprocessalways', function (e, data) {
        var index = data.index,
            file = data.files[index],
            node = $(data.context.children()[index]);
        if (file.error) {
            node
                .append('<br>')
                .append($('<span class="text-danger"/>').text(file.error));
        }
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Upload')
                .prop('disabled', !!data.files.error);
        }
        var images = document.getElementsByClassName("img_preview");
        for (var i = 0; i < images.length; i++) {
            anno.makeAnnotatable(images.item(i));
        }
    }).on('fileuploadprogressasll', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
    }).on('fileuploaddone', function (e, data) {
        $.each(data.result.files, function (index, file) {
            if (file.url) {
                var link = $('<a>')
                    .attr('target', '_blank')
                    .prop('href', file.url);
                $(data.context.children()[index])
                    .wrap(link);
            } else if (file.error) {
                var error = $('<span class="text-danger"/>').text(file.error);
                $(data.context.children()[index])
                    .append('<br>')
                    .append(error);
            }
        });
    }).on('fileuploadfail', function (e, data) {
        $.each(data.files, function (index) {
            var error = $('<span class="text-danger"/>').text('File upload failed.');
            $(data.context.children()[index])
                .append('<br>')
                .append(error);
        });
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});