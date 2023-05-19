function validateNumberInput(input) {
    // Remove non-numeric characters from the input value
    input.value = input.value.replace(/\D/g, '');
  }

function updateDiagnosisOptions() {
  var selectedMed = document.getElementById("med_input").value;
  var diagnosisInput = document.getElementById("diagnosis_input");
  
  // Clear existing options in the second select field
  diagnosisInput.innerHTML = "";
  
  // Create new options based on the selected value in the first select field
  switch (selectedMed) {
    case "hc_hadlock":
      addOption(diagnosisInput, "Macrocefalia", "macrocrania");
      addOption(diagnosisInput, "Microcefalia", "microcrania");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
      break;
    case "bpd_hadlock":
      addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
      addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
      break;
    case "csp":
      addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
      addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
      break;
    case "cm":
      addOption(diagnosisInput, "Megacisterno", "megacisterno");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
      break;
    case "vp":
      addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
      addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
      addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
      break;
    case "va":
      addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
      addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
      addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
      break;
    case "cereb_hill":
      addOption(diagnosisInput, "Hipoplasia cereberal", "hipoplasia");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
    break;
    case "afi":
      addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
      addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
    break;
    case "efw":
      addOption(diagnosisInput, "Feto grande", "feto-grande");
      addOption(diagnosisInput, "Feto pequeño", "feto-pequeño");
      addOption(diagnosisInput, "R.C.I.U", "rciu");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Todos", "todos");
    break;
    case "todas":
      addOption(diagnosisInput, "Todos", "todos");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Macrocefalia", "macrocrania");
      addOption(diagnosisInput, "Microcefalia", "microcrania");
      addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
      addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
      addOption(diagnosisInput, "Megacisterno", "megacisterno");
      addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
      addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
      addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
      addOption(diagnosisInput, "Hipoplasia cereberal", "hipoplasia");
      addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
      addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
      addOption(diagnosisInput, "Feto grande", "feto-grande");
      addOption(diagnosisInput, "Feto pequeño", "feto-pequeño");
      addOption(diagnosisInput, "R.C.I.U", "rciu");
    break;
    case "normal":
      addOption(diagnosisInput, "Todos", "todos");
      addOption(diagnosisInput, "Normal", "normal");
      addOption(diagnosisInput, "Macrocefalia", "macrocrania");
      addOption(diagnosisInput, "Microcefalia", "microcrania");
      addOption(diagnosisInput, "Anormalidad por valor superior", "anormal-sup");
      addOption(diagnosisInput, "Anormalidad por valor inferior", "anormal-inf");
      addOption(diagnosisInput, "Megacisterno", "megacisterno");
      addOption(diagnosisInput, "Ventriculomegalia leve", "ventri-leve");
      addOption(diagnosisInput, "Ventriculomegalia moderada", "ventri-mod");
      addOption(diagnosisInput, "Ventriculomegalia severa", "ventri-sev");
      addOption(diagnosisInput, "Hipoplasia cereberal", "hipoplasia");
      addOption(diagnosisInput, "Oligohidramnios", "oligohidramnios");
      addOption(diagnosisInput, "Polihidramnios", "polihidramnios");
      addOption(diagnosisInput, "Feto grande", "feto-grande");
      addOption(diagnosisInput, "Feto pequeño", "feto-pequeño");
      addOption(diagnosisInput, "R.C.I.U", "rciu");
    break;
    default:
      addOption(diagnosisInput, "Todos", "todas");
      break;
  }
}

function updateMedOptions() {
  var selectedDiagnosis = document.getElementById("diagnosis_input").value;
  var medInput = document.getElementById("med_input");
  
  // Clear existing options in the first select field
  medInput.innerHTML = "";
  
  // Create new options based on the selected value in the second select field
  switch (selectedDiagnosis) {
    case "normal":
      addOption(medInput, "Todas", "todas");
      addOption(medInput, "HC_HADLOCK", "hc_hadlock");
      addOption(medInput, "BPD_HADLOCK", "bpd_hadlock");
      addOption(medInput, "CSP", "csp");
      addOption(medInput, "CM", "cm");
      addOption(medInput, "VP", "vp");
      addOption(medInput, "VA", "va");
      addOption(medInput, "CEREB_HILL", "cereb_hill");
      addOption(medInput, "AFI", "afi");
      addOption(medInput, "EFW", "efw");
      break;
    case "todos":
      addOption(medInput, "Todas", "todas");
      addOption(medInput, "HC_HADLOCK", "hc_hadlock");
      addOption(medInput, "BPD_HADLOCK", "bpd_hadlock");
      addOption(medInput, "CSP", "csp");
      addOption(medInput, "CM", "cm");
      addOption(medInput, "VP", "vp");
      addOption(medInput, "VA", "va");
      addOption(medInput, "CEREB_HILL", "cereb_hill");
      addOption(medInput, "AFI", "afi");
      addOption(medInput, "EFW", "efw");
      break;
    case "macrocrania":
      addOption(medInput, "HC_HADLOCK", "hc_hadlock");
      addOption(medInput, "Todas", "todas");
      break;
    case "microcrania":
      addOption(medInput, "HC_HADLOCK", "hc_hadlock");
      addOption(medInput, "Todas", "todas");
      break;
    case "anormal-sup":
      addOption(medInput, "BPD_HADLOCK", "bpd_hadlock");
      addOption(medInput, "CSP", "csp");
      addOption(medInput, "Todas", "todas");
      break;
    case "anormal-inf":
      addOption(medInput, "BPD_HADLOCK", "bpd_hadlock");
      addOption(medInput, "CSP", "csp");
      addOption(medInput, "Todas", "todas");
      break;
    case "hipoplasia":
      addOption(medInput, "CEREB_HILL", "cereb_hill");
      addOption(medInput, "Todas", "todas");
      break;
    case "rciu":
      addOption(medInput, "EFW", "efw");
      addOption(medInput, "Todas", "todas");
      break;
    case "feto-grande":
      addOption(medInput, "EFW", "efw");
      addOption(medInput, "Todas", "todas");
      break;
    case "feto-pequeño":
      addOption(medInput, "EFW", "efw");
      addOption(medInput, "Todas", "todas");
      break;
    case "megacisterno":
      addOption(medInput, "CM", "cm");
      addOption(medInput, "Todas", "todas");
      break;
    case "ventri-leve":
      addOption(medInput, "VP", "vp");
      addOption(medInput, "VA", "va");
      addOption(medInput, "Todas", "todas");
      break;
    case "ventri-mod":
      addOption(medInput, "VP", "vp");
      addOption(medInput, "VA", "va");
      addOption(medInput, "Todas", "todas");
      break;
    case "ventri-sev":
      addOption(medInput, "VP", "vp");
      addOption(medInput, "VA", "va");
      addOption(medInput, "Todas", "todas");
      break;
    case "oligohidramnios":
      addOption(medInput, "AFI", "afi");
      addOption(medInput, "Todas", "todas");
      break;
    case "polihidramnios":
      addOption(medInput, "AFI", "afi");
      addOption(medInput, "Todas", "todas");
      break;
    // Add more cases for other selected values and their corresponding options
    // ...
    default:
      addOption(medInput, "Todas", "todas");
      break;
  }
}

// Function to add an option to a select element
function addOption(selectElement, text, value) {
  var option = document.createElement("option");
  option.text = text;
  option.value = value;
  selectElement.add(option);
}

