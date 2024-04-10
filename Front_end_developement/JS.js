let postsData = [];
const postsContainer = document.querySelector(".posts-container");

// Fetch SQL data?
fetch("Backend_API")
// Create an API endpoint (e.g., /api/posts) that queries the SQL database and returns the posts data in JSON format.
  .then(async (response) => {
    postsData = await response.json();
    postsData.map((post) => createPost(post));
  })
  .catch((error) => console.error("Error fetching data:", error));

const createPost = (postData) => {
  const { title, link, image, categories } = postData;
  const post = document.createElement("div");
  post.className = "post";
  post.innerHTML = `
    <a class="post-preview" href="${link}" target="_blank"> 
      <img class="post-image" src="${image}"> 
    </a> 
    <div class="post-content"> 
      <p class="post-title">${title}</p> 
      <div class="post-tags"> 
        ${categories
          .map((category) => {
            return '<span class="post-tag">' + category + "</span>";
          })
          .join("")} 
      </div> 
    </div>`;
  postsContainer.append(post);
};

// Function to filter posts based on search input
const filterPosts = (searchTerm) => {
  const filteredPosts = postsData.filter((post) =>
    post.title.toLowerCase().includes(searchTerm.toLowerCase())
  );
  postsContainer.innerHTML = "";
  filteredPosts.map((post) => createPost(post));
};

// Event listener for search input
const searchInput = document.querySelector("#search-input");
searchInput.addEventListener("input", (event) => {
  filterPosts(event.target.value);
});

const search = document.getElementById("search");
let debounceTimer;
const debounce = (callback, time) => {
  window.clearTimeout(debounceTimer);
  debounceTimer = window.setTimeout(callback, time);
};
search.addEventListener(
  "input",
  (event) => {
    const query = event.target.value;
    debounce(() => handleSearchPosts(query), 500);
  },
  false
);

function handleSearchPosts(query) {
    const searchQuery = query.trim().toLowerCase();

    if (searchQuery.length <= 1) {
        return;
    }
}

let searchResults = [...postsData].filter(
    (post) =>
      post.categories.some((category) => category.toLowerCase().includes(searchQuery)) ||
      post.title.toLowerCase().includes(query)
  );

  const searchDisplay = document.querySelector(".search-display");
  if (searchResults.length == 0) {
      searchDisplay.innerHTML = "No results found"
  } else if (searchResults.length == 1) {
      searchDisplay.innerHTML = `1 result found for your query: ${query}`
  } else {
      searchDisplay.innerHTML = `${searchResults.length} results found for your query: ${query}`
  }

  postsContainer.innerHTML = "";
searchResults.map((post) => createPost(post));

const resetPosts = () => {
    searchDisplay.innerHTML = ""
    postsContainer.innerHTML = "";
    postsData.map((post) => createPost(post));
  };
  const handleSearchPosts = (query) => {
    const searchQuery = query.trim().toLowerCase();
    
    if (searchQuery.length <= 1) {
      resetPosts()
      return
    }
    
    let searchResults = [...postsData].filter(
      (post) =>
        post.categories.some((category) => category.toLowerCase().includes(searchQuery)) ||
        post.title.toLowerCase().includes(searchQuery)
    );
    
    if (searchResults.length == 0) {
      searchDisplay.innerHTML = "No results found"
    } else if (searchResults.length == 1) {
      searchDisplay.innerHTML = `1 result found for your query: ${query}`
    } else {
      searchDisplay.innerHTML = `${searchResults.length} results found for your query: ${query}`
    }
    postsContainer.innerHTML = "";
    searchResults.map((post) => createPost(post));
  };