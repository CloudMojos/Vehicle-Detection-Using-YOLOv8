window.onload = function() {
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");
    const img = document.getElementById("scream");
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Draw the image scaled to fit the canvas

    const imageWidth = img.width; // Original image width
    const imageHeight = img.height; // Original image height

    console.log("Image width: ", imageWidth);
    console.log("Image height: ", imageHeight);

    const scaleX = imageWidth / canvas.width; // Calculate X-axis scaling factor
    const scaleY = imageHeight / canvas.height; // Calculate Y-axis scaling factor

    console.log("Scale X: ", scaleX);
    console.log("Scale Y: ", scaleY);

    document.getElementById("imgwidth").value = imageWidth
    document.getElementById("imgheight").value = imageHeight
    document.getElementById("canvaswidth").value = canvas.width
    document.getElementById("canvasheight").value = canvas.height

    const point1 = { x: 0, y: 0 };
    const point2 = { x: 0, y: 0 };
    const point3 = { x: 0, y: 0 };
    const point4 = { x: 0, y: 0 };

    const sliders = document.querySelectorAll('.slider'); // Get all sliders
    
    // Update point positions when sliders change
    sliders.forEach(slider => {
        slider.addEventListener("input", updatePoints);
    });

    function updatePoints() {
        point3.x = parseInt(slider5.value); // Scale x-coordinate
        point3.y = parseInt(slider6.value); // Scale y-coordinate
        point4.x = parseInt(slider7.value); // Scale x-coordinate
        point4.y = parseInt(slider8.value); // Scale y-coordinate

        // Redraw the canvas with updated points
        redrawCanvas();
    }
    
    function redrawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Redraw the scaled image
        
        // Draw points and lines using scaled coordinates
        ctx.fillStyle = "red"; // Set point color

        // Draw point 3
        ctx.fillRect(point3.x - 2.5, point3.y - 2.5, 5, 1); 


        // Draw point 4
        ctx.fillRect(point4.x - 2.5, point4.y - 2.5, 5, 1); 


        ctx.lineWidth = 5;

        ctx.beginPath();
        ctx.moveTo(point3.x, point3.y);
        ctx.lineTo(point4.x, point4.y);
        ctx.strokeStyle = "green";
        ctx.stroke();
    }
};