
// Recipe page js 
document.addEventListener('DOMContentLoaded', function() {
  // Bind click events to each button that toggles recipe details
  var buttons = document.querySelectorAll('button[data-target]');
  buttons.forEach(function(button) {
      button.addEventListener('click', function() {
          var targetId = this.getAttribute('data-target');
          var detailsDiv = document.getElementById(targetId);
          detailsDiv.classList.toggle('collapse');  // Toggle visibility of the recipe details
      });
  });
});


// This Js code was used from Driver.JS Tutorials 


    // This is still a WIP for the modals, still a bit buggy
    // window.addEventListener('DOMContentLoaded', function () {
    //   var loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    //   loginModal.show();
    // });
    const loginBtn = document.getElementById("loginBtn");
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));

    // Add an event listener to the login button
    loginBtn.addEventListener("click", function () {
      // Show the login modal when the button is clicked
      loginModal.show();
      // This is supposed to make the rest of the page active again once the 
      // modal is closed but it's not working yet
      loginModal.addEventListener('hidden.bs.modal', function () {
        document.body.style.overflow = 'auto';

      });
    });

// tour js 
const driver = window.driver.js.driver;

const driverObj = driver({
  showProgress: true,
  steps: [
    { element: '.nav', popover: { title: 'Get Started', description: "Let's take a quick tour to see what Foodie Hub is all about!" } },
    { element: '#recipeNav', popover: { title: 'Looking for something to eat?', description: 'Select from our delicious range of meals' } },
    { element: '#Recommed', popover: { title: 'Discover new places to eat', description: 'Want a new favourite restraunt? Click here!' } },
    { element: '#cus', popover: { title: 'Needing something more specific?', description: ' Click here, for more detailed recipes!' } },
    { element: '#users', popover: { title: 'Want to join us?', description: 'Looking to post, respond and keep connected? make sure to sign up or login' } },
    { element: '#logohome', popover: { title: 'Home Navigation', description: 'Want to navigate home, click here' } },
  ]
});


function startTour() {
  driverObj.drive(); // Start the tour
}

// Event listener for the "Start" button click
document.getElementById('start').addEventListener('click', startTour);


// JS code adapted from MapBox tutorials and chatgpt help
mapboxgl.accessToken = 'pk.eyJ1Ijoic3RldmkiLCJhIjoiY2x2ZWtrdThhMGI1bjJpbnFrNm9xem80YSJ9.Lz5tsAHEt_qZED_2_wyEGw';
const map = new mapboxgl.Map({
    container: 'map',
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [115.8605, -31.9505],
    zoom: 13
});

map.addControl(
    new MapboxDirections({
        accessToken: mapboxgl.accessToken
    }),
    'top-left'
  );


  

