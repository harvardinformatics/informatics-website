document.addEventListener('DOMContentLoaded', function() {
    // Array of image paths
    var images = [
        {path: 'img/banners/IMG_1445.jpg', position: 'center 25%'}, // Building windows 
        // {path: 'img/banners/IMG_1867.jpg', position: 'center 15%'}, // Pinnacle of building (Agassiz Hall/MCZ)
        {path: 'img/banners/IMG_2171.jpg', position: 'center 13%'}, // Divinity School building
        {path: 'img/banners/IMG_2177.jpg', position: 'center 70%'}, // "John Harvard" statue
        {path: 'img/banners/IMG_3075.jpg', position: 'center 48%'}, // Snowy Harvard Yard
        {path: 'img/banners/IMG_6113.jpg', position: 'center 75%'}, // Lawn chairs in snow
        {path: 'img/banners/IMG_6203.jpg', position: 'center 50%'}, // Widener Library
        // {path: 'img/banners/IMG_7402-HDR.jpg', position: 'center 50%'}, // Bottom of a brick archway
        {path: 'img/banners/IMG_7404.jpg', position: 'center 50%'}, // Flock of birds (default image)
        {path: 'img/banners/IMG_3764.jpg', position: 'center 50%'}, // Exterior of SEC
        {path: 'img/banners/IMG_0982.jpg', position: 'center 50%'}, // Spiral staircase in CGIS South
        {path: 'img/banners/IMG_3769.jpg', position: 'center 60%'}, // Vertex of Maxwell Dworkin on backdrop of sky
        {path: 'img/banners/IMG_3765.jpg', position: 'center 40%'}, // Interior of SEC
        {path: 'img/banners/IMG_3766.jpg', position: 'center 50%'}, // Art display in SEC
        {path: 'img/banners/bg08.jpg', position: 'center 50%'} // Italian trees
    ];

    var index = Math.floor(Math.random() * images.length);
    var image = images[index];
    var banner = document.querySelector('.banner-row-container');
    if(banner) { // Safety check
        banner.style.backgroundImage = 'url(' + image.path + ')';
        banner.style.backgroundPosition = image.position;
    }
});