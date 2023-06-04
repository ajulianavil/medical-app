var cardRadioButtonMap = new Map();

function handleRadioButton(radioButton) {

  var cardContainer = radioButton.closest('.card-two');
  var radioButtons = cardContainer.querySelectorAll('.right-div input[type="radio"]');
  //var totalCards = document.querySelectorAll('.card-two').length;

  var cardIndex = Array.from(document.querySelectorAll('.card-two')).indexOf(cardContainer);
  var radioButtonIndex = Array.from(radioButtons).indexOf(radioButton);

  if (isRadioButtonIndexValid(radioButtonIndex)) {
    return;
    radioButton.checked = false; 
  } else {
    console.log("here")
    cardRadioButtonMap.set(cardIndex, radioButtonIndex);
  }

  console.log('Card Index:', cardIndex);
  console.log('Radio Button Index:', radioButtonIndex);
  
  console.log(cardRadioButtonMap)

}

function isRadioButtonIndexValid(radioButtonIndex) {
  // Check if the radioButtonIndex is already present in the map for the given cardIndex
  return cardRadioButtonMap.has(radioButtonIndex);
}