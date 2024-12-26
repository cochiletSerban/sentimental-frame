const http = require("http");
const formidable = require("formidable");
const fs = require("fs");
const path = require("path");

const PORT = 3000;
const IMAGE_UPLOAD_DIR = path.join(__dirname, "../images");

// Ensure the upload directory exists
if (!fs.existsSync(IMAGE_UPLOAD_DIR)) {
    fs.mkdirSync(IMAGE_UPLOAD_DIR, { recursive: true });
}

// Create the server
const server = http.createServer((req, res) => {
    if (req.method === "GET") {
        // Serve the basic HTML upload form
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Image Upload</title>
            </head>
            <body>
                <h1>Upload Images</h1>
                <form action="/" method="POST" enctype="multipart/form-data">
                    <input type="file" name="images" multiple required>
                    <button type="submit">Upload</button>
                </form>
            </body>
            </html>
        `);
    } else if (req.method === "POST") {
        // Handle file uploads
        const form = new formidable.IncomingForm();
        form.uploadDir = IMAGE_UPLOAD_DIR; // Temporary directory
        form.keepExtensions = true;

        form.parse(req, (err, fields, files) => {
            if (err) {
                console.error("Error parsing files:", err);
                res.writeHead(500, { "Content-Type": "text/plain" });
                res.end("Internal Server Error");
                return;
            }

            // Process each uploaded file
            const uploadedFiles = Array.isArray(files.images) ? files.images : [files.images];
            uploadedFiles.forEach((file) => {
                const oldPath = file.filepath;
                const newPath = path.join(IMAGE_UPLOAD_DIR, file.originalFilename);
                fs.renameSync(oldPath, newPath); // Move file to the desired directory
                console.log(`Uploaded: ${file.originalFilename}`);
            });

            // Send response
            res.writeHead(200, { "Content-Type": "text/plain" });
            res.end("Files uploaded successfully!");
        });
    } else {
        res.writeHead(405, { "Content-Type": "text/plain" });
        res.end("Method Not Allowed");
    }
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});
