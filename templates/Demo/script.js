document.getElementById('downloadButton').addEventListener('click', function() {
    var fileUrl = "http://example.com/path/to/your/file.txt"; // Replace with your file URL
    var a = document.createElement('a');
    a.href = fileUrl;
    a.download = fileUrl.split('/').pop(); // This extracts the file name from the URL
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});
