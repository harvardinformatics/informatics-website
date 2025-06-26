document.addEventListener('DOMContentLoaded', function() {
    // Array of image paths
    var images = [
        {path: 'assets/img/banners/IMG_1445.jpg', position: 'center 25%'}, 
        {path: 'assets/img/banners/IMG_1867.jpg', position: 'center 15%'},
        {path: 'assets/img/banners/IMG_2171.jpg', position: 'center 13%'},
        {path: 'assets/img/banners/IMG_2177.jpg', position: 'center 70%'},
        {path: 'assets/img/banners/IMG_3075.jpg', position: 'center 48%'},
        {path: 'assets/img/banners/IMG_6113.jpg', position: 'center 75%'},
        {path: 'assets/img/banners/IMG_6203.jpg', position: 'center 50%'},
        {path: 'assets/img/banners/IMG_7402-HDR.jpg', position: 'center 50%'},
        {path: 'assets/img/banners/IMG_7404.jpg', position: 'center 50%'}
    ];

    var index = Math.floor(Math.random() * images.length);
    var image = images[index];
    var banner = document.querySelector('.banner-row-container');
    if(banner) { // Safety check
        banner.style.backgroundImage = 'url(' + image.path + ')';
        banner.style.backgroundPosition = image.position;
    }
});