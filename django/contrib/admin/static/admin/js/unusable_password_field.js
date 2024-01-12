"use strict";
// Fallback JS for browsers which do not support :has selector used in
// admin/css/unusable_password_fields.css
// Remove file once all supported browsers support :has selector
try {
    // If browser does not support :has selector this will raise an error
    document.querySelector("form:has(input)");
} catch (error) {
    // JS replacement for unsupported :has selector
    document.querySelectorAll('input[name="usable_password"]').forEach(option => {
        option.addEventListener('change', function() {
            const usable_password_selected = (this.value === "true" ? this.checked : !this.checked),
                submit1 = document.querySelector('input[type="submit"].set-password'),
                submit2 = document.querySelector('input[type="submit"].unset-password'),
                messages = document.querySelector('#id_unusable_warning');
            document.getElementById('id_password1').closest('.form-row').hidden = !usable_password_selected;
            document.getElementById('id_password2').closest('.form-row').hidden = !usable_password_selected;
            if (messages) {
                messages.hidden = usable_password_selected;
            }
            if (submit1 && submit2) {
                submit1.hidden = !usable_password_selected;
                submit2.hidden = usable_password_selected;
            }
        });
        option.dispatchEvent(new Event('change'));
    });
}
