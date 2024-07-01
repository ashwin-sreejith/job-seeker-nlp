  function toggleJobTypeInput() {
    // toggles visibility of jobType input field and related elements
    var jobTypeSection = document.getElementById('jobTypeSection');
    var submitButton = document.getElementById('submitButton');
    var errorLabel = document.getElementById('validationError');
    var form = document.getElementById('classifyForm');
    jobTypeSection.style.display = 'none';
    submitButton.style.display = 'none';
    errorLabel.style.display = 'none';
    form.reset();

  }

  function classifyJob() {
    // makes a post-request to get the classification of the given job ad
    const title = document.getElementById('jobTitle').value;
    const description = document.getElementById('jobDescription').value;

      // Check if both title and description have values
    if (!title.trim() || !description.trim()) {
        const errorElement = document.getElementById('validationError');
        errorElement.style.color = 'red';
        errorElement.textContent = 'Please fill in both Job Title and Job Description.';
        errorElement.style.display = 'block';
        errorElement.style.marginRight = '21rem';
        return;
    }
    // Get form data
    const formData = new FormData(document.getElementById('classifyForm'));

    // Send a POST request to the /classify route
    fetch('/classify', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Update the jobType input with the classified value
      document.getElementById('jobType').value = data.classifiedJobType;
      // Display the jobType section
      document.getElementById('jobTypeSection').style.display = 'block';
      document.getElementById('submitButton').style.display = 'block';
      document.getElementById('validationError').style.display = 'none'
    })
    .catch(error => console.error('Error:', error));
  }

  function addJob() {
    // adds a job to collection
    const title = document.getElementById('jobTitle').value;
    const description = document.getElementById('jobDescription').value;
    let company = document.getElementById('jobCompany').value;
    const category = document.getElementById('jobType').value.toLowerCase();
    const errorElement = document.getElementById('validationError');

    if (!title.trim() || !description.trim() || !category.trim()) {
        // ensures all fields have values
        errorElement.style.color = 'red';
        errorElement.textContent = 'Please fill in all the fields';
        errorElement.style.display = 'block';
        errorElement.style.marginRight = '21rem';
        return;
    }

    // only valid categories are allowed
    if (!(category === "sales" || category === "engineering" || category === "accounting" || category === "healthcare")) {
        errorElement.style.color = 'red';
        errorElement.textContent = 'Please choose a valid category';
        errorElement.style.display = 'block';
        errorElement.style.marginRight = '21rem';
        return;
    }

    // get form data
    const formData = new FormData(document.getElementById('classifyForm'));
    const categoryValue = formData.get('category').toLowerCase();
    // makes a post-request to /addJob route to add the post to collection
    formData.set('category', categoryValue);

      fetch('/addJob', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log('Job added successfully:', data);
        document.getElementById('validationError').style.display = 'block';
        document.getElementById('validationError').style.color = 'green';
        document.getElementById('validationError').textContent = "JobAd successfully Added";
        document.getElementById('jobTypeSection').style.display = 'none';
        document.getElementById('classifyForm').reset();

    })

    .catch(error => console.error('Error adding job:', error));
  }
