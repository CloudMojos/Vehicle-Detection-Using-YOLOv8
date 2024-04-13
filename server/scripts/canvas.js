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
        
        point1.x = parseInt(slider1.value) * (canvas.width / 600); // Scale x-coordinate
        point1.y = parseInt(slider2.value) * (canvas.height / 400); // Scale y-coordinate
        point2.x = parseInt(slider3.value) * (canvas.width / 600); // Scale x-coordinate
        point2.y = parseInt(slider4.value) * (canvas.height / 400); // Scale y-coordinate

        point3.x = parseInt(slider5.value) * (canvas.width / 600); // Scale x-coordinate
        point3.y = parseInt(slider6.value) * (canvas.height / 400); // Scale y-coordinate
        point4.x = parseInt(slider7.value) * (canvas.width / 600); // Scale x-coordinate
        point4.y = parseInt(slider8.value) * (canvas.height / 400); // Scale y-coordinate

        // Redraw the canvas with updated points
        redrawCanvas();
    }
    
    function redrawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Redraw the scaled image
        
        // Draw points and lines using scaled coordinates
        ctx.fillStyle = "red"; // Set point color
        // Draw point 1
        ctx.fillRect(point1.x - 2.5, point1.y - 2.5, 5, 1);
        
        // Draw point 2
        ctx.fillRect(point2.x - 2.5, point2.y - 2.5, 5, 1); 


        // Draw point 3
        ctx.fillRect(point3.x - 2.5, point3.y - 2.5, 5, 1); 


        // Draw point 4
        ctx.fillRect(point4.x - 2.5, point4.y - 2.5, 5, 1); 


        ctx.lineWidth = 5;
        
        // Draw lines between points
        ctx.beginPath();
        ctx.moveTo(point1.x, point1.y);
        ctx.lineTo(point2.x, point2.y);
        ctx.strokeStyle = "blue";
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(point3.x, point3.y);
        ctx.lineTo(point4.x, point4.y);
        ctx.strokeStyle = "green";
        ctx.stroke();
    }

    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit';
    submitButton.onclick = function() {
        const data = {
            point1: { x: point1.x * scaleX, y: point1.y * scaleY },
            point2: { x: point2.x * scaleX, y: point2.y * scaleY },
            point3: { x: point3.x * scaleX, y: point3.y * scaleY },
            point4: { x: point4.x * scaleX, y: point4.y * scaleY },
        };
        console.log(data); // Log data to console (replace with sending data to backend)
    };
};