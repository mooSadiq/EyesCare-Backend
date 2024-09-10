// alert
export function showAlert(icon, title, text, confirmButtonClass = 'btn btn-primary') {
  Swal.fire({
      icon: icon,
      title: title,
      text: text,
      customClass: {
          confirmButton: confirmButtonClass
      }
  });
}

// sweetalert

export async function showConfirmationDialog() {
  const result = await Swal.fire({
      title: 'هل أنت متأكد؟',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'نعم !',
      cancelButtonText: 'الغاء',
      customClass: {
          confirmButton: 'btn btn-primary me-3',
          cancelButton: 'btn btn-label-secondary'
      },
      buttonsStyling: false
  });
  return result;
}

