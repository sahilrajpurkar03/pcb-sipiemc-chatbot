
function sendMessage() {
  var messageInput = document.getElementById('message-input');
  var message = messageInput.value.trim();

  if (message !== '') {
    // Append the user message to the chat before sending it to Rasa
    appendMessage('User', message);

    fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({
          sender: 'user',
          message: message,
        }),
      })
      .then(response => response.json())
      .then(botResponses => {
        // Process and display bot responses
        botResponses.forEach(botResponse => {
          appendMessage('Bot', botResponse.text, botResponse.image, botResponse.source);
          if (botResponse.custom) {
            handleCustomCommand(botResponse.custom.command);
          }
        });
      })
      .catch(error => {
        console.error('Error sending message to Rasa:', error);
      });

    // Clear the message input
    messageInput.value = '';
  }
}

// Function to handle key press events
function handleKeyPress(event) {
  // Check if the pressed key is Enter (keyCode 13)
  if (event.keyCode === 13) {
    sendMessage();
  }
}

// Attach the handleKeyPress function to the keypress event of the message input
document.getElementById('message-input').addEventListener('keypress', handleKeyPress);

function appendMessage(sender, text, image, source) {
  var chatDisplay = document.getElementById('chat-display');
  var messageElement = document.createElement('div');
  messageElement.className = sender.toLowerCase() + '-message';

  // Check if an image URL is provided
  if (image) {
    var imgElement = document.createElement('img');
    imgElement.src = image;
    messageElement.appendChild(imgElement);
    messageElement.style.textAlign = 'center';
  }

  // Check if a source URL is provided
  if (source) {
    var sourceElement = document.createElement('a');
    sourceElement.href = source;
    sourceElement.textContent = "Source";
    sourceElement.target = "_blank";
    messageElement.appendChild(sourceElement);
  }

  // Check if text is provided
  if (text !== undefined) {
    var textElement = document.createElement('p');
    if (sender == 'Bot')
      textElement.innerHTML = '<strong>HAL:</strong> ' + text;
    else
      textElement.innerHTML = '<strong>' + sender + ':</strong> ' + text;
    messageElement.appendChild(textElement);

    if (text.includes('$')) {
      renderMathJax();
    }
  }

  chatDisplay.appendChild(messageElement);
  chatDisplay.scrollTop = chatDisplay.scrollHeight;
  MathJax.typeset([messageElement]);
}




////////////////////////////Function for Side Panel ///////////////////////

let windowsVisibility = {
  siWindowVisible: false,
  LTspiceWindowVisible: false,
  LTspice2WindowVisible: false
};

function hideAllWindows() {
  const windows = ['si-window', 'LTspice-window', 'LTspice2-window'];
  windows.forEach(windowId => {
    const windowElement = document.getElementById(windowId);
    if (windowElement) {
      windowElement.style.display = 'none';
    }
  });
  // Reset all visibility states
  for (let key in windowsVisibility) {
    if (windowsVisibility.hasOwnProperty(key)) {
      windowsVisibility[key] = false;
    }
  }
}

function toggleWindow(windowId) {
  const windowElement = document.getElementById(windowId);
  const overlay = document.getElementById('overlay');
  const visibilityKey = `${windowId.replace('-', '')}Visible`;

  if (windowsVisibility[visibilityKey]) {
    windowElement.style.display = 'none';
    overlay.style.display = 'none'; // Hide the overlay
    windowsVisibility[visibilityKey] = false;
  } else {
    hideAllWindows();
    windowElement.style.display = 'block';
    overlay.style.display = 'block'; // Show the overlay
    windowsVisibility[visibilityKey] = true;
  }
}

function handleButtonClick(buttonType) {
  if (buttonType === 'SI') {
    toggleWindow('si-window');
  } else if (buttonType === 'PI') {
    // Handle PI button click
    // Add functionality for PI button if needed
  } else if (buttonType === 'LTspice') {
    toggleWindow('LTspice-window');
  } else if (buttonType === 'LTspice2') {
    toggleWindow('LTspice2-window');
  }
}



///////////////////////////End Function for Side Panel ///////////////////////

///////////////////////////Function for SI Window/////////////////////////////

let currentSIHeading = '';

function handleSIButtonClick(siType) {
  // Update the heading based on the clicked button
  if (siType === 'Diff') {
    currentSIHeading = 'Differential Pair Circuit';
  } else if (siType === 'Single') {
    currentSIHeading = 'Single-ended Circuit';
  }

  // Call a function to update the SI window content
  updateSIWindow();
}

function updateSIWindow() {
  const siHeader = document.getElementById('si-header');
  const siImageContainer = document.getElementById('si-image-container');
  const diffForm = document.getElementById('diff-form');
  const singleForm = document.getElementById('single-form');
  const siForm = document.getElementById('si-form'); // Updated reference
  const generateButton = document.getElementById('si-sendecadstar');

  // Update the heading content
  siHeader.innerHTML = `<h2>${currentSIHeading}</h2>`;

  // Hide all images
  document.getElementById('image1').style.display = 'none';
  document.getElementById('image2').style.display = 'none';

  // Hide all forms initially
  diffForm.style.display = 'none';
  singleForm.style.display = 'none';
  generateButton.style.display = 'none';

  // Show the corresponding image based on the currentSIHeading
  if (currentSIHeading === 'Differential Pair Circuit') {
    document.getElementById('image1').style.display = 'block';
    diffForm.style.display = 'block';
    siForm.style.display = 'block';
    generateButton.style.display = 'block';
  } else if (currentSIHeading === 'Single-ended Circuit') {
    document.getElementById('image2').style.display = 'block';
    singleForm.style.display = 'block';
    siForm.style.display = 'block';
    generateButton.style.display = 'block';
  }
}

///////////////////////////End of Function for SI Window/////////////////

/////////////////////Function for send to ECADstar///////////////////////

function sendToECADStar() {
  // Collect input values based on your form structure
  var resistorR8Value = document.getElementById('resistorR8').value;
  var resistorR8Value = document.getElementById('resistorR9').value;
  var impedanceDL1Value = document.getElementById('impedanceDL1').value;
  var impedanceDL2Value = document.getElementById('impedanceDL2').value;
  var lengthDL1Value = document.getElementById('lengthDL1').value;
  var lengthDL2Value = document.getElementById('lengthDL2').value;

  // Construct the payload to be sent to the backend
  var payload = {
    R: resistorR8Value,
    w_dl1: impedanceDL1Value,
    w_dl2: impedanceDL2Value,
    length_dl1: lengthDL1Value,
    length_dl2: lengthDL2Value
  };

  // Send the payload to the backend
  fetch('/generate_eye_diagram', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
      displayEyeDiagram(data.imageUrl);
    })
    .catch(error => {
      console.error('Error sending data to backend:', error);
    });

}

function displayEyeDiagram(imageUrl) {
  var eyeDiagramContainer = document.getElementById('eye-diagram-container');
  eyeDiagramContainer.innerHTML = `<img src="${imageUrl}" alt="Eye Diagram">`;
}

///////////////////////////End of Function for send to ECADstar/////////////////////////////

////////////////////Function to Handle Custom Commands from RASA//////////////////////////

function handleCustomCommand(command) {
  switch (command) {
    case 'OPEN_STAR_TOPOLOGY':
      toggleWindow('LTspice-window');
      break;
    case 'OPEN_DAISY_CHAIN':
      toggleWindow('LTspice2-window');
      break;
    // Add more cases for other commands if needed
    default:
      console.warn('Unknown command:', command);
  }
}

///////////////////////////End Function to Handle Custom Commands//////////////////////////
