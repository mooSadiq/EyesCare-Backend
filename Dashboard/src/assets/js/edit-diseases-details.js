$(document).ready(function() {
    $('#editButton').click(function() {
        $(this).hide();
        $('#saveButton').show();
        $('#diseaseForm textarea, #diseaseForm input[type="file"]').prop('readonly', false).prop('disabled', false);
    });

    $('#saveButton').click(function() {
        $(this).hide();
        $('#editButton').show();
        $('#diseaseForm textarea, #diseaseForm input[type="file"]').prop('readonly', true).prop('disabled', true);
        // يمكنك إضافة شفرة لحفظ التعديلات هنا
        alert('تم حفظ التعديلات');
    });
   
    $('#diseaseImages').change(function() {
        $('#imagePreview').empty();
        var files = this.files;
        var preview = $('#imagePreview');
        if (files.length > 0) {
            if (files.length == 1) {
                preview.addClass('single-image').removeClass('multiple-images');
            } else {
                preview.addClass('multiple-images').removeClass('single-image');
            }
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                var reader = new FileReader();
                reader.onload = function(e) {
                    var img = $('<img>').attr('src', e.target.result);
                    preview.append(img);
                }
                reader.readAsDataURL(file);
            }
        }
    });
});