function displayImage(imageURL, locX, locY) {
  const contentSection = document.querySelector(".map-image");

  const image = `<img src="${imageURL}" alt="Map Image" id="img">`;
  contentSection.innerHTML = image;

  const element = document.getElementById("map-image");
  const rect = element.getBoundingClientRect();
  const offsetX = rect.left;
  const offsetY = rect.top;
  const pin = `<div class="pin" style="left: ${offsetX + locX - 20}px; top: ${offsetY + locY - 20}px;"></div>`;
  contentSection.innerHTML += pin;

  const descriptionSection = document.getElementById("description");
  let text = "Description not found."

  if(imageURL.endsWith("A0.png"))
    text = "Floor 0 in builduing A (Koszykowa 86).";
  else if(imageURL.endsWith("A1.png"))
    text = "Floor 1 in builduing A (Koszykowa 86).";
  else if(imageURL.endsWith("A2.png"))
    text = "Floor 2 in builduing A (Koszykowa 86).";
  else if(imageURL.endsWith("A3.png"))
    text = "Floor 3 in builduing A (Koszykowa 86).";
  else if(imageURL.endsWith("A4.png"))
    text = "Floor 4 in builduing A (Koszykowa 86).";


descriptionSection.innerHTML = text;
}

function displayAll(){
  const contentSection = document.querySelector(".map-image");

  let image = `<img src="http://127.0.0.1:8001/img/A0.png" alt="Map Image" id="img">`;
  image += `<img src="http://127.0.0.1:8001/img/A1.png" alt="Map Image" id="img">`;
  image += `<img src="http://127.0.0.1:8001/img/A2.png" alt="Map Image" id="img">`;
  image += `<img src="http://127.0.0.1:8001/img/A3.png" alt="Map Image" id="img">`;
  image += `<img src="http://127.0.0.1:8001/img/A4.png" alt="Map Image" id="img">`;
  contentSection.innerHTML = image;

  const descriptionSection = document.getElementById("description");
  let text = "These are all the maps."
  descriptionSection.innerHTML = text;

}
