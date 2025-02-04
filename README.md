[![](./chat.svg)](https://twitter.com/daverndn)

### Hi there👋 I'm [Dave](https://linkedin.com/in/daverndn), a Microsoft MVP, author, and blogger who focuses on Azure architecture and cloud solutions.

[![YouTube Subscribe](https://img.shields.io/badge/YouTube_@azinsider-SUBSCRIBE-red?logo=youtube&style=for-the-badge&logoColor=red)](https://www.youtube.com/azinsider?sub_confirmation=1) 

[![X](https://img.shields.io/badge/@daverndn-000000?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/intent/follow?original_referer=https%3A%2F%2Fgithub.com%Fdaverndn&screen_name=daverndn)

[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz1Dfbvqa7aG2YPlnKTwriQ?label=YouTube%20Views&style=for-the-badge)](https://youtube.com/azinsider)


### Let's connect!
[![Linkedin Follow](https://img.shields.io/static/v1?label=&message=Linkedin&color=blue&logo=linkedin&style=for-the-badge)](https://linkedin.com/in/daverndn)
[![MVP Follow](https://img.shields.io/static/v1?label=&message=MicrosoftMVP&color=blue&logo=microsoft&style=for-the-badge)](https://mvp.microsoft.com/en-us/PublicProfile/5000671?fullName=David%20Rend%C3%B3n)


---

### 📚 Recent [books](https://amazon.com/author/daverendon):
 - 📘[Azure Architecture Explained: A comprehensive guide to building effective cloud solutions](https://amzn.to/4863Ped)
 - 📘[Azure for Decision Makers: The essential guide to Azure for business leaders](https://amzn.to/3EzgiJZ)
 - 📘[Building Applications with Azure Resource Manager (ARM)](https://amzn.to/448fO8n)
 - 📘[Pro Azure Governance and Security](https://amzn.to/3XfsSGR)
 - 📘[Microsoft AI MVP Book](https://amzn.to/3NbPLX2)
 - 📘[Azure Strategy and Implementation Guide, 4th edition](https://amzn.to/3pgcAAU)

 
---

### GitHub Stats

![](http://github-stats-dr.vercel.app/api/cards/profile-details?username=daverendon&theme=aura)
![](http://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=daverendon&theme=aura)
![](http://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=daverendon&theme=aura)
![](http://github-stats-dr.vercel.app/api/cards/stats?username=daverendon&theme=aura)

<!---
![](https://azinsider-github-readme-stats.vercel.app/api?username=daverendon&theme=aura)
-->
<br /><br />

---

### 📚 Recent [Blog posts](https://blog.azinsider.net)


<div id="posts">
                                <!-- Blog posts will be inserted here by JavaScript -->
                              </div>
                              <script>
                                // --- Configuration and Caching Variables ---
                                const FEED_URL = 'https://medium.com/feed/@daverendon';
                                // Use CORS Anywhere proxy.
                                const CORS_PROXY = 'https://cors-anywhere.herokuapp.com/';
                                const CACHE_KEY = 'mediumFeed';
                                const CACHE_TIMESTAMP_KEY = 'mediumFeedTimestamp';
                                const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
                            
                                // --- Function to Parse and Display the Feed ---
                                function displayPosts(xmlString) {
                                  // Parse the XML string into a DOM document.
                                  const parser = new DOMParser();
                                  const xmlDoc = parser.parseFromString(xmlString, "application/xml");
                            
                                  // Try to select RSS <item> elements; if not found, try Atom <entry> elements.
                                  let items = xmlDoc.querySelectorAll("item");
                                  if (!items || items.length === 0) {
                                    items = xmlDoc.querySelectorAll("entry");
                                  }
                            
                                  const postsContainer = document.getElementById("posts");
                                  postsContainer.innerHTML = '';
                            
                                  // Loop through the first 12 items.
                                  for (let i = 0; i < Math.min(12, items.length); i++) {
                                    const item = items[i];
                            
                                    // Get the title.
                                    const titleEl = item.querySelector("title");
                                    const title = titleEl ? titleEl.textContent : 'No Title';
                            
                                    // Get the link.
                                    let link = '';
                                    const linkEl = item.querySelector("link");
                                    if (linkEl) {
                                      // For RSS feeds, the link is the text content.
                                      link = linkEl.textContent.trim();
                                      // For Atom feeds, the link might be in an attribute.
                                      if (!link && linkEl.getAttribute('href')) {
                                        link = linkEl.getAttribute('href');
                                      }
                                    }
                            
                                    // Get the publication date: <pubDate> in RSS or <updated> in Atom.
                                    let pubDate = '';
                                    if (item.querySelector("pubDate")) {
                                      pubDate = item.querySelector("pubDate").textContent;
                                    } else if (item.querySelector("updated")) {
                                      pubDate = item.querySelector("updated").textContent;
                                    }
                            
                                    // Create the HTML structure for a single post.
                                    const postDiv = document.createElement("div");
                                    postDiv.className = "post";
                            
                                    const postTitle = document.createElement("h2");
                                    postTitle.className = "post-title";
                                    postTitle.textContent = title;
                                    postDiv.appendChild(postTitle);
                            
                                    const postDate = document.createElement("div");
                                    postDate.className = "post-date";
                                    // Format the date nicely.
                                    const dateObj = new Date(pubDate);
                                    postDate.textContent = dateObj.toLocaleDateString();
                                    postDiv.appendChild(postDate);
                            
                                    const readMore = document.createElement("a");
                                    readMore.className = "read-more";
                                    readMore.textContent = "Read More";
                                    readMore.href = link;
                                    readMore.target = "_blank"; // Open in a new tab.
                                    postDiv.appendChild(readMore);
                            
                                    postsContainer.appendChild(postDiv);
                                  }
                                }
                            
                                // --- Function to Fetch the Feed ---
                                function fetchFeed() {
                                  fetch(CORS_PROXY + FEED_URL)
                                    .then(response => {
                                      if (!response.ok) {
                                        throw new Error('Network response was not ok: ' + response.statusText);
                                      }
                                      return response.text();
                                    })
                                    .then(xmlString => {
                                      // Cache the feed and current timestamp in localStorage.
                                      localStorage.setItem(CACHE_KEY, xmlString);
                                      localStorage.setItem(CACHE_TIMESTAMP_KEY, Date.now());
                                      displayPosts(xmlString);
                                    })
                                    .catch(error => {
                                      console.error("Error fetching feed:", error);
                                      document.getElementById("posts").innerHTML = "<p>Error fetching posts.</p>";
                                    });
                                }
                            
                                // --- Check Cache and Load Feed ---
                                const cachedFeed = localStorage.getItem(CACHE_KEY);
                                const cachedTimestamp = localStorage.getItem(CACHE_TIMESTAMP_KEY);
                            
                                // If the feed is cached and is less than 24 hours old, use it; otherwise, fetch a fresh copy.
                                if (cachedFeed && cachedTimestamp && (Date.now() - cachedTimestamp < CACHE_DURATION)) {
                                  displayPosts(cachedFeed);
                                } else {
                                  fetchFeed();
                                }
                              </script>

                              <style>
    /* Basic styling for the page and posts */
    body {
      font-family: Arial, sans-serif;
      background-color: #f8f8f8;
      margin: 20px;
    }
    h1 {
      text-align: center;
    }
    .post {
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 15px;
      margin: 15px auto;
      max-width: 600px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .post-title {
      font-size: 1.3em;
      margin: 0 0 10px;
    }
    .post-date {
      color: #777;
      font-size: 0.9em;
      margin-bottom: 10px;
    }
    .read-more {
      display: inline-block;
      background-color: #28a745;
      color: #fff;
      padding: 8px 12px;
      text-decoration: none;
      border-radius: 4px;
      transition: background-color 0.3s ease;
    }
    .read-more:hover {
      background-color: #218838;
    }
  </style>



<div id="articles"> 
  <a target="_blank" href="https://blog.azinsider.net"><img src="https://medium-snippet-dc633c4f39a0.herokuapp.com/api/article.svg?username=@daverendon&index=0&source=medium" alt="Recent Article 0" style="float:left;width:'300px'; padding: '5px';"> 

 <a target="_blank" href="https://blog.azinsider.net/"><img src="https://medium-snippet-dc633c4f39a0.herokuapp.com/api/article.svg?username=@daverendon&index=1&source=medium" alt="Recent Article 1" style="float:left;width:'300px'; padding: '5px'"> 

<a target="_blank" href="https://blog.azinsider.net/"><img src="https://medium-snippet-dc633c4f39a0.herokuapp.com/api/article.svg?username=@daverendon&index=2&source=medium" alt="Recent Article 2" style="float:left;width:'300px'; padding: '5px';"> 

<a target="_blank" href="https://blog.azinsider.net/"><img src="https://medium-snippet-dc633c4f39a0.herokuapp.com/api/article.svg?username=@daverendon&index=3&source=medium" alt="Recent Article 3" style="float:left;width:'300px'; padding: '5px';"> 
</div> 
           

<!--
**daveRendon/daverendon** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
