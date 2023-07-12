var cardRadioButtonMap = new Map();

function handleRadioButton(radioButton) {

  var cardContainer = radioButton.closest('.card-two');
  var radioButtons = cardContainer.querySelectorAll('.right-div input[type="radio"]');
  //var totalCards = document.querySelectorAll('.card-two').length;

  var cardIndex = Array.from(document.querySelectorAll('.card-two')).indexOf(cardContainer);
  var radioButtonIndex = Array.from(radioButtons).indexOf(radioButton);

  console.log(cardIndex, radioButtonIndex)

  var radioId = 'radio_' + cardIndex + '_' + radioButtonIndex;
  var radd = document.getElementById(radioId);
  cardRadioButtonMap.set(cardIndex, radioButtonIndex);

  // var xx = document.getElementById(radioId);
  console.log("xx", radd)

  if (isRadioButtonIndexValid(radioButtonIndex)) {
    cardRadioButtonMap.forEach(function(value, key){
      console.log(value, key)

      var elementId = 'radio' + radioButtonIndex;

      var radioButton = document.getElementById(elementId);

      if (radioButton) {
        console.log("rad", radioButton)
        // Perform operations on the radio button element
        radioButton.checked = true;
        // ... additional operations ...
      }
    });
    // radioButton.checked = false; 
  } else {
    console.log("here")
    cardRadioButtonMap.set(cardIndex, radioButtonIndex);
  }

  console.log('Card Index:', cardIndex);
  console.log('Radio Button Index:', radioButtonIndex);
  
  console.log("cardmap", cardRadioButtonMap)
}

function isRadioButtonIndexValid(radioButtonIndex) {
  // Check if the radioButtonIndex is already present in the map for the given cardIndex
  return cardRadioButtonMap.has(radioButtonIndex);
}