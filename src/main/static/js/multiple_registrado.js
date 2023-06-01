function handleRadioButton(radioButton) {
  var cardContainer = radioButton.closest('.card-two');
  var radioButtons = cardContainer.querySelectorAll('.right-div input[type="radio"]');
  var totalCards = document.querySelectorAll('.card-two').length;

  // Get the index of the clicked radio button within its card
  var radioButtonIndex = Array.from(radioButtons).indexOf(radioButton);

  // Calculate the index of the corresponding radio button on the second card
  var correspondingCardIndex = (Array.from(document.querySelectorAll('.card-two')).indexOf(cardContainer) + 1) % totalCards;
  var correspondingCard = document.querySelectorAll('.card-two')[correspondingCardIndex];
  var correspondingRadioButtons = correspondingCard.querySelectorAll('.right-div input[type="radio"]');
  var correspondingRadioButtonIndex = (radioButtonIndex + 1) % correspondingRadioButtons.length;

  // Find the corresponding radio button on the second card
  var correspondingRadioButton = correspondingRadioButtons[correspondingRadioButtonIndex];

  // Check or uncheck the corresponding radio button based on the clicked radio button's status
  if (radioButton.checked && correspondingRadioButton) {
    correspondingRadioButton.checked = true;
  } else if (!radioButton.checked && correspondingRadioButton) {
    correspondingRadioButton.checked = false;
  }
}
