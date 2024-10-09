/**
 * Selects & Tags
 */

'use strict';

$(function () {
  const selectPicker = $('.selectpicker'),
    fieldSelect = $('.fieldSelect2'),
    jornalSelect = $('.jornalSelect2'),
    select2Icons = $('.select2-icons');

  // Bootstrap Select
  // --------------------------------------------------------------------
  if (selectPicker.length) {
    selectPicker.selectpicker();
  }

  // Select2
  // --------------------------------------------------------------------

  // Default
  if (jornalSelect.length) {
    jornalSelect.each(function () {
      var $this = $(this);
      $this.wrap('<div class="position-relative"></div>').select2({
        placeholder: 'اختر المجلة',
        dropdownParent: $this.parent()
      });
    });
  }
  // Default
  if (fieldSelect.length) {
    fieldSelect.each(function () {
      var $this = $(this);
      $this.wrap('<div class="position-relative"></div>').select2({
        placeholder: 'اختر المجال',
        dropdownParent: $this.parent()
      });
    });
  }

  // Select2 Icons
  if (select2Icons.length) {
    // custom template to render icons
    function renderIcons(option) {
      if (!option.id) {
        return option.text;
      }
      var $icon = "<i class='" + $(option.element).data('icon') + " me-2'></i>" + option.text;

      return $icon;
    }
    select2Icons.wrap('<div class="position-relative"></div>').select2({
      dropdownParent: select2Icons.parent(),
      templateResult: renderIcons,
      templateSelection: renderIcons,
      escapeMarkup: function (es) {
        return es;
      }
    });
  }
});
