document.addEventListener('DOMContentLoaded', function() {
    var banners = window.SCHEDULED_BANNERS;
    if (!banners || !banners.length) { // Safety check
        return;
    }

    var now = new Date();
    var dismissedKeyPrefix = 'scheduledBannerDismissed:';

    var active = banners.filter(function(banner) {
        if (!banner.enabled) {
            return false;
        }
        var start = new Date(banner.start + 'T00:00:00');
        var end = new Date(banner.end + 'T23:59:59');
        if (now < start || now > end) {
            return false;
        }
        if (banner.dismissable && localStorage.getItem(dismissedKeyPrefix + banner.id)) {
            return false;
        }
        return true;
    });

    if (!active.length) {
        return;
    }

    var wrapper = document.createElement('div');
    wrapper.id = 'scheduled-banner-wrapper';

    active.forEach(function(banner) {
        var row = document.createElement('div');
        row.className = 'scheduled-banner';
        row.setAttribute('data-banner-id', banner.id);

        var content = document.createElement('span');
        content.className = 'scheduled-banner-content';
        content.innerHTML = banner.html;
        row.appendChild(content);

        if (banner.dismissable) {
            var closeButton = document.createElement('button');
            closeButton.className = 'scheduled-banner-close';
            closeButton.setAttribute('aria-label', 'Dismiss announcement');
            closeButton.innerHTML = '&times;';
            closeButton.addEventListener('click', function() {
                localStorage.setItem(dismissedKeyPrefix + banner.id, '1');
                row.remove();
                if (!wrapper.querySelector('.scheduled-banner')) {
                    wrapper.remove();
                }
            });
            row.appendChild(closeButton);
        }

        wrapper.appendChild(row);
    });

    var header = document.querySelector('.md-header');
    if (header) { // Safety check
        header.insertAdjacentElement('beforebegin', wrapper);
    } else {
        document.body.insertAdjacentElement('afterbegin', wrapper);
    }
});
