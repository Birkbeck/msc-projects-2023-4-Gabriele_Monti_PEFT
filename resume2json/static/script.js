const textGenForm = document.querySelector(".chat-form");


const translateText = async (text) => {
  
 //const inferResponse = await fetch(`gemmac64?input=${text}`);
 const inferResponse = await fetch(`https://theoracle-resume-2-json.hf.space/gemmac64?input=${encodeURIComponent(text)}`);
 if (!inferResponse.ok) {
  console.error('Response error:', inferResponse.status);
  return "Error processing your request. Please try again.";
}


 const inferJson = await inferResponse.json();

  return inferJson.output;
};

textGenForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const textGenInput = document.getElementById("chat-input");
  console.log("Form submitted");
  const textGenParagraph = document.querySelector(".chat-output");

  textGenParagraph.textContent = await translateText(textGenInput.value);
});


