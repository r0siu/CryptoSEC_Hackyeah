
    // Add event listener to radio buttons
  // JavaScript to handle page switching and loading content
  const pageLinks = document.querySelectorAll('.nav-link');
  const contentContainer = document.getElementById('content');


  // Function to load content from a specific page
  function loadPageContent(pageName) {
    fetch(`${pageName}.html`)
            .then(response => response.text())
            .then(data => {
              // Insert the content into the content container
              contentContainer.innerHTML = data;
            })
            .catch(error => console.error(error));

  }

  // Load base.html content by default
  loadPageContent('base');

  pageLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();

      // Get the page name from the link's ID
      const pageName = link.id.replace('-link', '');

      // Load the content for the selected page
      loadPageContent(pageName);
    });
  });

  const buttons = document.querySelectorAll('.nav-link');

function resetMenuColors() {
    buttons.forEach(button => {
        button.classList.remove('active');
        button.classList.add('text-white');
    });
}

function handleClick(event) {
    resetMenuColors();
    event.target.classList.add('active');
}

buttons.forEach(button => {
    button.addEventListener('click', handleClick);
});


function sendData() {
    const form = document.getElementById('pkcsForm');
    const formData = new FormData(form);

    // Add a file to the form data (assuming you have an input with type="file" in your form)
    const fileInput = document.querySelector('input[type="file"]');
    const files = fileInput.files;

    // Append each selected file to the form data
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    // User authentication data TODO: change this to actually use user & secret
    // const user = document.getElementById('user').value;
    // const secret = document.getElementById('secret').value;
    const user = 'adam';
    const secer = 'rosiek';
    // Generate a JWT token with user credentials
    // const token = generateJWT(user, secret);
    const token = 'tokenisko';

    // Construct headers with JWT token
    const headers = new Headers();
    headers.append('Authorization', 'Bearer ' + token);

    const apiUrl = 'http://127.0.0.1:5000/api/v1/document/encrypt';

     // Send a POST request to the REST API with form data and JWT token in headers
    fetch(apiUrl, {
        method: 'POST',
        body: formData,
        headers: headers,
    })
    .then(response => {
        // Check if the response contains a file attachment
        const contentDisposition = response.headers.get('Content-Disposition');
        console.log(contentDisposition);
        if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
            // Extract the filename from the Content-Disposition header
            const filename = contentDisposition.split('filename=')[1].trim();

            // Create a blob from the response data
            return response.blob().then(blob => {
                // Create a URL for the blob
                const blobUrl = window.URL.createObjectURL(blob);

                // Create a temporary <a> element to trigger the download
                const a = document.createElement('a');
                a.href = blobUrl;
                a.download = 'downloaded_file.pdf'; // TODO: maybe fix filename
                a.style.display = 'none';
                document.body.appendChild(a);

                // Trigger the download
                console.log("Downloading a file: ");
                console.log(filename);
                a.click();

                // Clean up
                window.URL.revokeObjectURL(blobUrl);
                document.body.removeChild(a);
            });
        } else {
            // Handle other types of responses here
            // For example, you can parse response text or handle errors
            return response.text().then(text => {
                console.log("Sukcesowy zwrot ale nie pliku");
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerHTML = 'An error occurred.';
    });

}

