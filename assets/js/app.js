import emailSpellChecker from './emailSpellCheck'

dismiss_alert = function (e) {
    e.closest('.alert-dismissible').remove()
}

// Timezone settings. See TimezoneMiddleware in utils/middleware.py
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone // e.g. "America/New_York"
document.cookie = `totem_timezone=${timezone}; SameSite=Strict`

window.addEventListener('DOMContentLoaded', () => {
    emailSpellChecker()
})
