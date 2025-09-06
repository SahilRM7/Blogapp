async function generateBlog() {
  const prompt = document.getElementById("promptInput").value;
  const outputDiv = document.getElementById("blogOutput");
  const loadingDiv = document.getElementById("loading");

  if (!prompt.trim()) {
    alert("Please enter a topic!");
    return;
  }

  loadingDiv.style.display = "block";
  outputDiv.innerHTML = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/generate-blog", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();

    if (data.blog) {
      outputDiv.innerHTML = formatBlog(data.blog);
    } else {
      outputDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
    }
  } catch (err) {
    outputDiv.innerHTML = `<p style="color:red;">Failed to connect to backend</p>`;
  }

  loadingDiv.style.display = "none";
}

function formatBlog(text) {
  // Split text into paragraphs for readability
  const paragraphs = text.split("\n").filter(p => p.trim());
  return paragraphs.map(p => `<p>${p}</p>`).join("");
}
