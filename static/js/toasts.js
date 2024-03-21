(function () {
    var toastElements = document.getElementsByClassName('toast')

    for (const toastElement of toastElements) {
        const toast = new bootstrap.Toast(toastElement, {delay: 9500})
        toast.show()
    }

})()
